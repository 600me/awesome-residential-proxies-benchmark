import sys, time, os
from pathlib import Path

sys.path.insert(0, "/home/kais/x-matrix-runtime(X矩阵运行器)")
from x_matrix_lx_engine import Socks5AuthBridge, launch_context, _wait_login_input

proxy_pass = os.environ.get("PROXY_PASS", "***")
bridge = Socks5AuthBridge("198.37.116.128", 6087, "vsunwqqv", proxy_pass)
local_port = bridge.start()
from patchright.sync_api import sync_playwright

test_account = os.environ.get("TEST_X_ACCOUNT", "test_operator@example.com")
test_chal = os.environ.get("TEST_X_CHALLENGE", "test_user")

with sync_playwright() as pw:
    context = launch_context(pw, Path("/tmp/test_err_text"), local_port, "", {"width": 1280, "height": 720})
    try:
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://x.com/i/flow/login", wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
        inp = _wait_login_input(page, 15000)
        inp.fill(test_account)
        time.sleep(1)
        for b in page.query_selector_all("button, [role=button]"):
            if b.is_visible() and b.text_content().strip() == "Continue":
                b.click()
                break
        time.sleep(3)
        chal = page.wait_for_selector("input[name='challenge_response']", timeout=10000)
        chal.click()
        page.keyboard.type(test_chal, delay=50)
        print("Input value before click:", repr(chal.input_value()))
        time.sleep(1)

        # Inspect and click via JS
        for p in page.query_selector_all('p:text-is("Continue")'):
            if p.is_visible():
                info = p.evaluate("""el => {
                    const parent = el.parentElement;
                    const grandparent = parent ? parent.parentElement : null;
                    return {
                        pText: el.innerText,
                        parentTag: parent ? parent.tagName : null,
                        parentRole: parent ? parent.getAttribute('role') : null,
                        parentDisabled: parent ? parent.getAttribute('disabled') : null,
                        parentAriaDisabled: parent ? parent.getAttribute('aria-disabled') : null,
                        parentClasses: parent ? parent.className : null,
                        gpTag: grandparent ? grandparent.tagName : null,
                        gpHtml: grandparent ? grandparent.outerHTML.slice(0, 300) : null
                    };
                }""")
                print("Continue button element tree:\n", info)
                # Try clicking parent via JS dispatch
                p.evaluate("el => (el.closest('button') || el.parentElement).click()")
                print("JS clicked parent/button!")
                break
        time.sleep(4)
        print("URL after JS click:", page.url)
        print("Full innerText after JS click:\n", page.evaluate("() => document.body.innerText")[:500])
    finally:
        context.close()
        bridge.stop()
