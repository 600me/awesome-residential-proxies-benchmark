#!/usr/bin/env python3
"""
Rigid Execution Deployer for Track 3: Hugging Face (Spaces + Datasets) & GitHub Gist Parasite Matrix

1. Push hf-space-mirror to Hugging Face Spaces (600me/llm-gpu-cost-calculator & 600me/residential-proxy-sticky-session-calculator)
2. Push hf-dataset-mirror to Hugging Face Datasets (600me/developer-coupons-breakdown)
3. Run 11-Brand Gist expansion verification
4. Verify public HTTP endpoints
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
import requests

ROOT = Path("/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark")
SPACE_MIRROR = ROOT / "hf-space-mirror"
STICKY_MIRROR = ROOT / "hf-space-sticky-mirror"
DATASET_MIRROR = ROOT / "hf-dataset-mirror"
GIST_EXPANDER = ROOT / "coupon-parasite-pages(优惠码寄生截流页)" / "expand-gists(扩铺Gist与验收).py"

def get_hf_token():
    env_file = Path("/Users/a600/.secrets(密钥)/huggingface-token.env")
    assert env_file.exists(), "Missing HF token file"
    m = re.search(r"HF_TOKEN\s*=\s*([^\s]+)", env_file.read_text())
    assert m, "Invalid HF token format"
    return m.group(1).strip()

def push_git_repo(source_dir, remote_url, commit_msg):
    tmp_git = tempfile.mkdtemp(prefix="hf-git-")
    try:
        # Copy files to temp directory
        for item in source_dir.iterdir():
            if item.name == ".git":
                continue
            dest = Path(tmp_git) / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

        # Git operations
        run = lambda cmd: subprocess.run(cmd, cwd=tmp_git, check=True, capture_output=True, text=True)
        run(["git", "init", "-b", "main"])
        run(["git", "config", "user.name", "600me"])
        run(["git", "config", "user.email", "600megd@gmail.com"])
        run(["git", "add", "."])
        run(["git", "commit", "-m", commit_msg])
        run(["git", "remote", "add", "origin", remote_url])
        # Push to main
        push_res = subprocess.run(["git", "push", "-f", "origin", "main"], cwd=tmp_git, capture_output=True, text=True)
        assert push_res.returncode == 0, f"Git push failed: {push_res.stderr}"
        return True, "Push successful"
    except Exception as exc:
        return False, str(exc)
    finally:
        shutil.rmtree(tmp_git, ignore_errors=True)

def verify_url(url, expected_code=200):
    try:
        r = requests.get(url, timeout=15)
        return r.status_code == expected_code, r.status_code
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 60)
    print("  Starting Track 3 Hugging Face & Gist Production Deployment")
    print("=" * 60)

    hf_token = get_hf_token()
    results = {}

    # 1. Deploy Hugging Face Spaces (Space 1: 4-Track General Calculator, Space 2: Dedicated Sticky Session Calculator)
    spaces_to_deploy = [
        ("600me/llm-gpu-cost-calculator", SPACE_MIRROR, f"https://600me:{hf_token}@huggingface.co/spaces/600me/llm-gpu-cost-calculator", "Deploy 2026 Developer Infrastructure & Cloud TCO Benchmark Calculator"),
        ("600me/residential-proxy-sticky-session-calculator", STICKY_MIRROR, f"https://600me:{hf_token}@huggingface.co/spaces/600me/residential-proxy-sticky-session-calculator", "Deploy 2026 Residential Proxy Sticky Session & Concurrency Loss Calculator")
    ]
    for name, source_dir, remote, commit_msg in spaces_to_deploy:
        print(f"Deploying Space: {name} from {source_dir.name} ...")
        ok, msg = push_git_repo(source_dir, remote, commit_msg)
        time.sleep(2)
        public_url = f"https://huggingface.co/spaces/{name}"
        v_ok, code = verify_url(public_url)
        results[f"space_{name}"] = {"pushed": ok, "public_url": public_url, "http_status": code, "verified": v_ok}
        print(f" -> Result: pushed={ok}, public_status={code}")

    # 2. Deploy Hugging Face Dataset
    dataset_name = "600me/developer-coupons-breakdown"
    dataset_remote = f"https://600me:{hf_token}@huggingface.co/datasets/{dataset_name}"
    print(f"\nDeploying Dataset: {dataset_name} ...")
    ok, msg = push_git_repo(DATASET_MIRROR, dataset_remote, "Update 2026 Developer Cloud Infrastructure & True TCO Benchmark (14 Brands)")
    time.sleep(2)
    public_url = f"https://huggingface.co/datasets/{dataset_name}"
    v_ok, code = verify_url(public_url)
    results[f"dataset_{dataset_name}"] = {"pushed": ok, "public_url": public_url, "http_status": code, "verified": v_ok}
    print(f" -> Result: pushed={ok}, public_status={code}")

    # 3. Run Gist expansion verification
    print(f"\nRunning Gist expansion engine: {GIST_EXPANDER} ...")
    gist_res = subprocess.run([sys.executable, str(GIST_EXPANDER)], capture_output=True, text=True)
    print(gist_res.stdout)
    results["gist_expansion_code"] = gist_res.returncode
    results["gist_verification_path"] = str(ROOT / "coupon-parasite-pages(优惠码寄生截流页)" / "expansion-verification(扩铺与报告验收).json")

    # Final summary
    print("\n" + "=" * 60)
    print("  Deployment Execution Summary")
    print("=" * 60)
    for k, v in results.items():
        print(f"{k}: {v}")

    return 0 if all(v.get("verified", True) for v in results.values() if isinstance(v, dict)) else 1

if __name__ == "__main__":
    sys.exit(main())
