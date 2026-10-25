#!/usr/bin/env python3
"""Submit and independently read back the five authorized one-line wave2 PRs."""
import argparse
import base64
import datetime
import difflib
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "submitted_prs.jsonl"
BRANCH = "add-check-proxy-tax-wave2"
ENTRY = "[check-proxy-tax](https://github.com/600me/check-proxy-tax) - Zero-dependency CLI (PyPI & Node.js) auditing effective proxy cost, usable request ratio, and anti-bot latency."
TARGETS = [
    ("lorien/awesome-web-scraping", "python.md", "## Proxy Tools", "append", "*"),
    ("BruceDone/awesome-crawler", "README.md", "## Python", "append", "*"),
    ("atinfo/awesome-test-automation", "general-purpose-test-automation-tools.md", "## Performance and load testing", "alphabetical", "*"),
    ("yosriady/awesome-api-devtools", "README.md", "## API Testing", "alphabetical", "-"),
    ("dastergon/awesome-sre", "README.md", "## Monitoring & Observability & Alerting", "append", "*"),
]


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def api(path, payload=None, method=None, expected=None):
    assert path.startswith("/")
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request("https://api.github.com" + path, data=data,
        method=method, headers={"Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json", "User-Agent": "600me-awesome-wave2",
        "X-GitHub-Api-Version": "2022-11-28", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            status = response.status
            result = json.load(response)
    except urllib.error.HTTPError as error:
        # Report GitHub's response, never request headers or credentials.
        raise RuntimeError(f"GitHub {error.code} {path}: {error.read().decode()}") from None
    if expected is not None:
        assert status == expected, (path, status, expected)
    return result, status


def get(path):
    return api(path, expected=200)[0]


def addition(text, section, ordering, bullet):
    assert "github.com/600me/check-proxy-tax" not in text, "Already listed"
    lines = text.splitlines(keepends=True)
    start = next(i for i, line in enumerate(lines) if line.strip() == section)
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].startswith("## ")), len(lines))
    items = [i for i in range(start + 1, end) if re.match(r"^[*-] \[", lines[i])]
    assert items, (section, "No existing list items")
    index = items[-1] + 1
    if ordering == "alphabetical":
        index = next((i for i in items if re.match(r"^[*-] \[([^]]+)\]", lines[i])
                     .group(1).lower() > "check-proxy-tax"), index)
    newline = "\r\n" if "\r\n" in text else "\n"
    lines.insert(index, bullet + " " + ENTRY + newline)
    updated = "".join(lines)
    diff = list(difflib.unified_diff(text.splitlines(), updated.splitlines()))
    assert [line for line in diff if line.startswith("+") and not line.startswith("+++")] == ["+" + bullet + " " + ENTRY]
    assert not [line for line in diff if line.startswith("-") and not line.startswith("---")]
    return updated, diff


def save(record):
    lines = LEDGER.read_text().splitlines(keepends=True)
    for i, line in enumerate(lines):
        old = json.loads(line)
        if old.get("wave") == "wave2" and old["repo"] == record["repo"]:
            lines[i] = json.dumps(record, ensure_ascii=False) + "\n"
            LEDGER.write_text("".join(lines))
            return
    with LEDGER.open("a") as output:
        output.write(json.dumps(record, ensure_ascii=False) + "\n")
        output.flush()
        os.fsync(output.fileno())


def verify(repo, number, path):
    pr = get(f"/repos/{repo}/pulls/{number}")
    files = get(f"/repos/{repo}/pulls/{number}/files")
    assert pr["state"] == "open" and not pr["merged"]
    assert (pr["changed_files"], pr["additions"], pr["deletions"]) == (1, 1, 0)
    assert len(files) == 1 and files[0]["filename"] == path
    added = [line[1:] for line in files[0]["patch"].splitlines()
             if line.startswith("+") and not line.startswith("+++")]
    assert len(added) == 1 and added[0][2:] == ENTRY
    assert pr["base"]["ref"] == "master"
    return pr


def main(submit, verify_only):
    assert get("/user")["login"] == "600me"
    for repo, path, section, ordering, bullet in TARGETS:
        metadata = get("/repos/" + repo)
        assert not metadata["archived"]
        if verify_only:
            rows = [json.loads(line) for line in LEDGER.read_text().splitlines()]
            record, = [r for r in rows if r.get("wave") == "wave2" and r["repo"] == repo]
            verify(repo, record["pr_number"], path)
            print("VERIFIED", record["pr_url"], "open 1 file +1 -0", flush=True)
            continue
        query = urllib.parse.quote(f'repo:{repo} is:pr "check-proxy-tax"')
        matches = get("/search/issues?q=" + query)["items"]
        prs = get(f"/repos/{repo}/pulls?state=all&head=600me:{BRANCH}")
        assert not [p for p in matches if p["number"] not in {p["number"] for p in prs}], "Prior suggestion exists"
        status = None
        if prs:
            assert len(prs) == 1
            pr = verify(repo, prs[0]["number"], path)
        else:
            base = get(f"/repos/{repo}/git/ref/heads/master")["object"]["sha"]
            contents = get(f"/repos/{repo}/contents/{path}?ref={base}")
            original = base64.b64decode(contents["content"]).decode()
            updated, diff = addition(original, section, ordering, bullet)
            print(repo, path, section, "\n" + "\n".join(diff), flush=True)
            if not submit:
                continue
            fork, _ = api(f"/repos/{repo}/forks", {"default_branch_only": True}, expected=202)
            fork_name = fork["full_name"]
            assert fork["owner"]["login"] == "600me"
            for attempt in range(15):
                try:
                    get(f"/repos/{fork_name}/git/commits/{base}")
                    break
                except RuntimeError:
                    if attempt == 14:
                        raise
                    time.sleep(2)
            refs = get(f"/repos/{fork_name}/git/matching-refs/heads/{BRANCH}")
            if refs:
                ref, = [r for r in refs if r["ref"] == "refs/heads/" + BRANCH]
                head = ref["object"]["sha"]
            else:
                tree = get(f"/repos/{repo}/git/commits/{base}")["tree"]["sha"]
                new_tree, _ = api(f"/repos/{fork_name}/git/trees", {"base_tree": tree,
                    "tree": [{"path": path, "mode": "100644", "type": "blob", "content": updated}]}, expected=201)
                commit, _ = api(f"/repos/{fork_name}/git/commits", {
                    "message": "Add check-proxy-tax to " + section.lstrip("# "),
                    "tree": new_tree["sha"], "parents": [base]}, expected=201)
                head = commit["sha"]
                api(f"/repos/{fork_name}/git/refs", {"ref": "refs/heads/" + BRANCH, "sha": head}, expected=201)
            compare = get(f"/repos/{repo}/compare/{base}...600me:{head}")
            changed, = compare["files"]
            assert (changed["filename"], changed["additions"], changed["deletions"]) == (path, 1, 0)
            assert "+" + bullet + " " + ENTRY in changed["patch"].splitlines()
            body = f"Adds check-proxy-tax to `{path}` under **{section.lstrip('# ')}**.\n\n{bullet} {ENTRY}\n\nI maintain check-proxy-tax. This PR adds exactly one list entry and changes no existing lines."
            if repo == "lorien/awesome-web-scraping":
                body += "\n\nAge disclosure: the project was created on 2026-10-18 and is currently younger than the one-month requirement in CONTRIBUTING.md. This submission requests consideration with that limitation explicitly disclosed."
            pr, status = api(f"/repos/{repo}/pulls", {"title": "Add check-proxy-tax to " + section.lstrip("# "),
                "head": "600me:" + BRANCH, "base": "master", "body": body}, expected=201)
            save({"wave": "wave2", "repo": repo, "pr_number": pr["number"], "pr_url": pr["html_url"],
                  "state": pr["state"], "creation_http_status": status, "recorded_at": now()})
            pr = verify(repo, pr["number"], path)
        previous = [json.loads(line) for line in LEDGER.read_text().splitlines()]
        receipt = next((r for r in previous if r.get("wave") == "wave2" and r["repo"] == repo), {})
        receipt.update({"wave": "wave2", "repo": repo, "stars": metadata["stargazers_count"],
            "pr_number": pr["number"], "pr_url": pr["html_url"], "state": pr["state"],
            "changed_files": pr["changed_files"], "additions": pr["additions"], "deletions": pr["deletions"],
            "branch": "600me:" + BRANCH, "base_branch": "master", "commit_sha": pr["head"]["sha"],
            "asset": "check-proxy-tax", "asset_url": "https://github.com/600me/check-proxy-tax",
            "title": pr["title"], "created_at": pr["created_at"], "verified_at": now(),
            "verified_via": "GitHub REST API PR details and files", "path": path, "section": section})
        save(receipt)
        print("VERIFIED", pr["html_url"], "open 1 file +1 -0", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    TOKEN = re.search(r"GITHUB_TOKEN\s*=\s*(\S+)", Path(
        "/Users/a600/.secrets(密钥)/github-token(GitHub发帖令牌).env").read_text()).group(1)
    main(args.submit, args.verify_only)
