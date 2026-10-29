import os
import sys
import json
import subprocess

BASE_DIR = "/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark"
PACKS_DIR = os.path.join(BASE_DIR, "coupon-parasite-pages(优惠码寄生截流页)", "surround-packs(1号4仓包围网待发包)")

with open("/tmp/phase4_shortlinks.json", "r", encoding="utf-8") as f:
    SHORTLINKS = json.load(f)

BANNED = ["dusen.party", "norb.date", "zelumo.top", "plue.men", "272738.xyz", "mybskm.top", "600me", "src="]

def assert_clean(text, context):
    for b in BANNED:
        if b in text:
            raise ValueError(f"CRITICAL REDLINE: {b} found in {context}")

def write_repo(brand, repo_name, calc_script_name, calc_code, readme_text):
    repo_dir = os.path.join(PACKS_DIR, brand, repo_name)
    os.makedirs(repo_dir, exist_ok=True)
    
    assert_clean(calc_code, f"{brand}/{repo_name}/{calc_script_name}")
    assert_clean(readme_text, f"{brand}/{repo_name}/README.md")
    
    words = len(readme_text.split())
    if words < 450:
        raise ValueError(f"WORD COUNT TOO LOW: {brand}/{repo_name}/README.md has only {words} words (minimum 450 required)")
        
    script_path = os.path.join(repo_dir, calc_script_name)
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(calc_code.strip() + "\n")
    os.chmod(script_path, 0o755)
    
    readme_path = os.path.join(repo_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_text.strip() + "\n")
        
    res = subprocess.run(["python3", script_path], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Calculator failed to execute: {script_path}\n{res.stderr}")
    print(f"Generated {brand}/{repo_name} (Words: {words}, Calc: OK)")

print("Build script harness created.")
