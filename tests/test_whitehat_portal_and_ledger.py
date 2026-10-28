"""Read-only acceptance checks against public pages and the dated evidence ledger.

No browser, credentials, affiliate registration, tax submission or redirected
vendor requests are used. Network failures fail acceptance rather than skip it.
"""
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / 'competitor-hunter(同行反查器)/affiliate_master_ledger(联盟母平台与品牌开通总账本).json'
REPORT = Path('/Users/a600/project-hub(项目设计实施)/kais-business-findings(生意发现记录)/cps-affiliate-onboarding-ledger-20261028(海外CPS联盟母平台与新品牌开通总账).md')
ARTICLE_NAMES = {
    'enterprise-residential-proxy-latency-tco-2026.html',
    'serverless-gpu-h100-inference-cost-analysis.html',
    'multi-account-antidetect-browser-isolation-architecture.html',
    'ai-ad-creative-pipeline-unit-economics.html',
    'us-business-formation-compliance-tco-non-residents.html',
    'b2b-social-listening-and-lead-intelligence-stack.html',
}
NEW_ROUTES = [f'https://{host}/{prefix}/{number}'
              for host, prefix in [('dusen.party', 'a'), ('norb.date', 'p'), ('zelumo.top', 'c')]
              for number in range(1, 5)]


def normalized_text(content):
    """Decode only Cloudflare email obfuscation; preserve the underlying content."""
    soup = BeautifulSoup(content, 'html.parser')
    for anchor in soup.select('a.__cf_email__[data-cfemail]'):
        data = bytes.fromhex(anchor['data-cfemail'])
        anchor.replace_with(bytes(x ^ data[0] for x in data[1:]).decode('utf-8'))
    for script in soup.select('script[src="/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js"]'):
        script.decompose()
    return ' '.join(soup.get_text(' ', strip=True).split())


def test_cloudflare_normalization_preserves_email_and_detects_content_change():
    protected = '<p><a class="__cf_email__" data-cfemail="016041632f626e6c">protected</a></p>'
    assert normalized_text(protected) == normalized_text('<p>a@b.com</p>')
    assert normalized_text(protected) != normalized_text('<p>different@b.com</p>')


@pytest.fixture(scope='module')
def ledger():
    return json.loads(LEDGER.read_text())


@pytest.fixture(scope='module')
def live(ledger):
    observations = ledger['portal']['pages'] + ledger['gateways']
    urls = [item['url'] for item in observations]
    assert len(urls) == len(set(urls)), 'Duplicate evidence URLs'

    def get(url):
        response = requests.get(url, timeout=40, allow_redirects=False)
        assert not response.history, 'Must not follow affiliate or registration redirects'
        return url, response

    with ThreadPoolExecutor(max_workers=10) as pool:
        return dict(pool.map(get, urls))


def test_directive_and_verified_affiliate_links_obtained(ledger):
    directive = ledger['directive']
    assert '只拿到联盟链接' in directive['text']
    assert directive['verified_affiliate_links_extracted'] == 3
    brands = {row['name']: row for row in ledger['brands']}
    networks = {row['name']: row for row in ledger['networks']}
    assert brands['AdsPower']['status'] == 'ENABLED_REFERRAL_CODE_VERIFIED'
    assert brands['AdsPower']['affiliate_url'] == 'https://www.adspower.net/share/bGrcRR'
    assert brands['9Proxy']['status'] == 'ENABLED_REFERRAL_CODE_VERIFIED'
    assert brands['9Proxy']['affiliate_url'] == 'https://9proxy.com/sign-up?inviteCode=9P_K4a0sawT'
    assert brands['Pawns']['status'] == 'ENABLED_REFERRAL_CODE_VERIFIED'
    assert brands['Pawns']['affiliate_url'] == 'https://pawns.app/?r=20796407'
    assert networks['LemonSqueezy']['status'] == 'APPLICATION_SUBMITTED_UNDER_REVIEW'
    assert networks['Impact']['status'] == 'DEFERRED_PER_USER_DIRECTIVE'
    assert ledger['commercial_outcome']['new_affiliate_links_obtained_this_run'] == 3
    assert ledger['commercial_outcome']['new_approvals_this_run'] == 3


def test_article_inventory_and_home_links(ledger, live):
    pages = ledger['portal']['pages']
    articles = [p for p in pages if '/benchmarks/' in p['url']]
    assert ledger['portal']['article_count'] == len(articles) == 6
    assert {urlsplit(p['url']).path.rsplit('/', 1)[-1] for p in articles} == ARTICLE_NAMES
    assert len(pages) == 9
    home = BeautifulSoup(live['https://proxy.mybskm.top/'].content, 'html.parser')
    paths = {urlsplit(a['href']).path for a in home.select('a[href]')}
    assert {'/benchmarks/' + name for name in ARTICLE_NAMES} <= paths
    assert {'/about.html', '/privacy.html'} <= paths


@pytest.mark.parametrize('path', ['/', '/about.html', '/privacy.html'] +
                         ['/benchmarks/' + name for name in sorted(ARTICLE_NAMES)])
def test_live_portal_content_matches_recorded_evidence(path, ledger, live):
    url = 'https://proxy.mybskm.top' + path
    record = next(p for p in ledger['portal']['pages'] if p['url'] == url)
    response = live[url]
    assert response.status_code == record['http_status'] == 200
    assert re.fullmatch(r'[0-9a-f]{64}', record['sha256'])
    assert hashlib.sha256(normalized_text(response.content).encode()).hexdigest() == record['content_text_sha256']
    assert datetime.fromisoformat(record['checked_at']).tzinfo
    assert record['method'] == 'GET' and record['redirects_followed'] is False
    local_content = (ROOT / record['local_path']).read_bytes()
    assert hashlib.sha256(local_content).hexdigest() == record['local_source_sha256']
    assert hashlib.sha256(normalized_text(local_content).encode()).hexdigest() == record['content_text_sha256']
    soup = BeautifulSoup(response.content, 'html.parser')
    assert soup.title.get_text() == record['title']
    if '/benchmarks/' in path:
        assert soup.html.get('lang') == 'en'
        main = soup.select_one('main')
        assert main and main.find('h2') and main.find('table')
        words = len(re.findall(r"\b[A-Za-z]+(?:['’-][A-Za-z]+)*\b", main.get_text(' ', strip=True)))
        assert words == record['word_count'] and words > 0
        for term in ['coupon', 'promo code', 'discount']:
            assert len(re.findall(term, response.text, re.I)) == record['forbidden_counts'][term] == 0
        assert 'noindex' not in response.headers.get('X-Robots-Tag', '').lower()
        assert all('noindex' not in m.get('content', '').lower()
                   for m in soup.select('meta[name="robots"]'))


@pytest.mark.parametrize('url', NEW_ROUTES)
def test_new_gateway_is_302_affiliate_redirect(url, ledger, live):
    record = next(g for g in ledger['gateways'] if g['url'] == url)
    response = live[url]
    assert response.status_code == record['http_status'] == 302
    assert response.headers['Location'] == record['location']
    destination = urlsplit(response.headers['Location'])
    expected_host = {'dusen.party': 'www.adspower.net', 'norb.date': '9proxy.com',
                     'zelumo.top': 'pawns.app'}[urlsplit(url).hostname]
    assert destination.scheme == 'https' and destination.hostname == expected_host
    assert record['attribution_class'] == 'VERIFIED_AFFILIATE_LINK'


def test_existing_gateway_evidence_is_live_without_following(ledger, live):
    old_routes = [g for g in ledger['gateways'] if urlsplit(g['url']).hostname == 'go.272738.xyz']
    assert old_routes
    for record in old_routes:
        response = live[record['url']]
        assert response.status_code == record['http_status']
        assert response.status_code in (301, 302)
        assert response.headers['Location'] == record['location']
        assert record['redirects_followed'] is False
        assert urlsplit(record['location']).scheme == 'https'


def test_tax_evidence_preserves_uncertainty_and_zero_balances(ledger):
    tax = ledger['partnerstack']
    assert tax['status'] == 'TAX_LOCATION_REQUIRED'
    assert tax['required_action_summary'] == '必须填写税务登记位置以提现'
    assert '必须填写税务注册位置' in tax['visible_tax_notice']
    assert '填写税务信息以提现' == tax['visible_payout_notice']
    assert tax['source_url'] == 'https://dash.partnerstack.com/payouts/rewards'
    assert tax['w8ben_status'] == tax['payment_binding_status'] == 'NOT_VERIFIED'
    assert tax['available_funds_usd'] == tax['commission_total_usd'] == 0
    assert tax['home_observation']['Firstbase.io'] == '已启用'
    assert tax['home_observation']['Bright Data'] == tax['home_observation']['Doola'] == '申请待处理'
    assert ledger['portal']['content_benchmark_claims_independently_verified'] is False


def test_historical_source_preserved_and_report_consistent(ledger):
    history = ledger['historical_records']
    source = ROOT / history['source_path']
    assert hashlib.sha256(source.read_bytes()).hexdigest() == history['source_sha256']
    assert history['brands'] == json.loads(source.read_text())['brands']
    assert history['verification_status'] == 'HISTORICAL_ONLY_NOT_CURRENT_ACCOUNT_PROOF'
    assert ledger['report_path'] == str(REPORT)
    report = REPORT.read_text()
    for record in ledger['portal']['pages']:
        assert f'| {record["url"]} | {record["http_status"]} | {record["word_count"]} |' in report
    for record in ledger['gateways']:
        assert f'| {record["url"]} | {record["http_status"]} | {record["location"]} |' in report
    for record in ledger['networks'] + ledger['brands']:
        assert f'| {record["name"]} | {record["status"]} |' in report
    for text in ['必须填写税务登记位置以提现', 'NOT_VERIFIED', '800', '未注册、未提交联盟申请',
                 'Pi DeepSeek-V4.1', '不宣称外部模型审计已经完成']:
        assert text in report
