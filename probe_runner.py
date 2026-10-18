#!/usr/bin/env python3
"""Small async proxy benchmark; config uses the JSON subset of YAML."""
import argparse
import asyncio
from collections import Counter
from datetime import datetime, timezone
import ipaddress
import json
import os
from pathlib import Path
import statistics
import tempfile
import time

import aiohttp

ROOT = Path(__file__).resolve().parent
START = '<!-- BENCHMARK:START -->'
END = '<!-- BENCHMARK:END -->'


async def request(session, url, proxy=None):
    started = time.perf_counter()
    try:
        async with session.get(url, proxy=proxy) as response:
            latency = (time.perf_counter() - started) * 1000
            body = await response.text()
            return response.status, latency, body, 'OK' if 200 <= response.status < 300 else 'Failed'
    except asyncio.TimeoutError:
        return None, None, '', 'Timeout'
    except (aiohttp.ClientError, ValueError, OSError):
        # Never print exception text: proxy URLs can contain credentials.
        return None, None, '', 'Failed'


async def classify(session, body):
    try:
        address = ipaddress.ip_address(json.loads(body)['ip'])
        status, _, raw, _ = await request(session, f'https://api.ipapi.is/?q={address}')
        data = json.loads(raw)
        if not isinstance(data, dict):
            return 'Unknown (unexpected lookup response)'
        if status != 200 or data.get('error') or data.get('is_bogon'):
            return 'Unknown (lookup unavailable / limited)'
        asn = data.get('asn') or {}
        company = data.get('company') or {}
        asn = asn if isinstance(asn, dict) else {}
        company = company if isinstance(company, dict) else {}
        label = 'Unknown'
        if data.get('is_datacenter') is True or company.get('type') == 'hosting':
            label = 'Hosting'
        elif company.get('type') == 'isp' or asn.get('type') == 'isp':
            label = 'ISP (residential candidate)'
        return f"{label}; AS{asn.get('asn', '?')}"
    except (ValueError, KeyError, TypeError):
        return 'Unknown (lookup unavailable / limited)'


async def probe(session, vendor, config, direct=False):
    proxy = None if direct else os.environ.get(vendor['proxy_env'])
    if not direct and not proxy:
        return vendor, 'Not configured', '—', '—', 'Unknown', 'Not tested'
    results = await asyncio.gather(*(request(session, config['target_url'], proxy) for _ in range(config['attempts'])))
    successes = [r for r in results if r[3] == 'OK']
    latencies = [r[1] for r in results if r[1] is not None]
    statuses = ', '.join(f'{s}×{n}' for s, n in Counter(str(r[0]) if r[0] else r[3] for r in results).items())
    kind = await classify(session, successes[0][2]) if successes else 'Unknown'
    outcome = 'OK' if len(successes) == len(results) else ('Timeout' if all(r[3] == 'Timeout' for r in results) else 'Failed')
    return vendor, f'{len(successes) / len(results):.1%} ({len(successes)}/{len(results)})', f'{statistics.median(latencies):.0f}' if latencies else '—', statuses, kind, outcome


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ').replace('\r', ' ')


def render(rows):
    lines = [f"Updated: {datetime.now(timezone.utc).isoformat(timespec='seconds')} (UTC)", '',
             '**Live run — unconfigured vendors are not tested.**', '',
             '| Provider / action | Success Rate | Latency ms (headers, median) | HTTP status | IP / ASN | Result | Promo Code |',
             '|---|---:|---:|---|---|---|---|']
    for vendor, rate, latency, status, kind, outcome in rows:
        name = f"[{vendor['name']}]({vendor['referral_url']})" if vendor.get('referral_url') else vendor['name']
        lines.append('| ' + ' | '.join(map(cell, [name, rate, latency, status, kind, outcome, vendor.get('promo_code', '—')])) + ' |')
    return '\n'.join(lines)


def inject(table):
    path = ROOT / 'README.md'
    original = path.read_text(encoding='utf-8')
    if original.count(START) != 1 or original.count(END) != 1 or original.index(START) >= original.index(END):
        raise ValueError('README must contain one ordered benchmark marker pair')
    before, rest = original.split(START)
    _, after = rest.split(END)
    updated = before + START + '\n\n' + table + '\n\n' + END + after
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=ROOT, delete=False) as output:
            temporary = output.name
            output.write(updated)
            output.flush()
            os.fsync(output.fileno())
        os.chmod(temporary, path.stat().st_mode & 0o777)
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)


async def main(dry_run):
    config = json.loads((ROOT / 'config/affiliates.yaml').read_text(encoding='utf-8'))
    if not isinstance(config['attempts'], int) or not 1 <= config['attempts'] <= 10:
        raise ValueError('attempts must be between 1 and 10')
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
        direct = await probe(session, {'name': 'Direct (real network)'}, config, direct=True)
        if dry_run:
            rows = [direct]
            rows.extend((vendor, 'Not tested', '—', '—', 'Unknown', 'Not tested')
                        for vendor in config['vendors'])
            print(render(rows))
            print('Local dry run: README not modified; run without --dry-run for a live table.')
            return
        vendor_rows = await asyncio.gather(*(probe(session, vendor, config) for vendor in config['vendors']))
        rows = [direct, *vendor_rows]
    inject(render(rows))
    print('README benchmark updated')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    asyncio.run(main(parser.parse_args().dry_run))
