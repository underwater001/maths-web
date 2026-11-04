#!/usr/bin/env python3
"""Browser test of the site: loads it from a local server and clicks through the web, the bank and search.

    python3 tools/render_test.py [screenshot_dir]

Needs Playwright and Chrome. If the CDN is unreachable (as in the build sandbox) it serves d3 from a local copy
(set D3_PATH) and blocks the fonts, so three font errors in the console are expected and ignored.
"""
import functools, http.server, json, os, socketserver, sys, threading
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = sys.argv[1] if len(sys.argv) > 1 else None
D3 = open(os.environ.get("D3_PATH", "/opt/npm-tools/node_modules/d3/dist/d3.min.js")).read()
CHROME = os.environ.get("CHROME_PATH", "/usr/bin/google-chrome")


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def log_message(self, *a): pass


srv = socketserver.TCPServer(("127.0.0.1", 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
errs, reqs, fails = [], [], []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond: fails.append(msg)


def route(r):
    u = r.request.url
    if "cdnjs.cloudflare.com" in u and "d3" in u: r.fulfill(body=D3, content_type="application/javascript")
    elif "fonts.g" in u: r.abort()
    else:
        reqs.append(u); r.continue_()


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
    def page(w, h, scheme="light"):
        c = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme); pg = c.new_page()
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "ERR_FAILED" not in m.text and "fonts" not in m.text else None)
        pg.on("pageerror", lambda e: errs.append("PAGEERROR " + str(e)))
        pg.route("**/*", route); pg.goto(f"http://127.0.0.1:{port}/index.html"); pg.wait_for_selector(".nd", timeout=15000); pg.wait_for_timeout(500); return pg
    core = json.load(open(os.path.join(ROOT, "data", "core.json")))
    nbank = len(core["bank"]["rows"])
    pg = page(1280, 900)
    check(not any("/shards/" in u for u in reqs), "start-up fetches no topic shard (lazy loading)")
    check(f"{nbank} questions in the bank" in pg.inner_text("#panel h2"), f"overview says {nbank} questions in the bank")
    check(pg.locator(".ring").count() >= 9, f"built nodes are ringed ({pg.locator('.ring').count()})")
    pg.locator('.nd[data-id="profit-loss"]').click(); pg.wait_for_timeout(500)
    check(any("shards/profit-loss" in u for u in reqs) and not any("shards/partnership" in u for u in reqs), "opening Profit & Loss fetches only its own shard")
    check("This topic" in pg.inner_text("#panel") and "of 3 shifts" in pg.inner_text("#panel"), "topic panel shows how often it was asked")
    pg.locator('#panel .chip[data-go="c-pl-multiplier"]').click(); pg.wait_for_timeout(200)
    check(pg.locator("#panel .formula").count() == 5, f"concept shows its 5 formulas ({pg.locator('#panel .formula').count()})")
    pg.locator('#panel .chip[data-go="q-pl-chain"]').click(); pg.wait_for_timeout(300)
    check(pg.locator("#panel .qz").count() == 4 + 5, f"Markup-discount type shows 4 PYQs + 5 practice ({pg.locator('#panel .qz').count()})")
    check(pg.locator("#panel .ledger dt", has_text="Variations").count() == 1, "method ledger lists variations to expect")
    card = pg.locator("#panel .qz").first; key = card.get_attribute("data-key")
    wrong = [k for k in "abcd" if k != key][0]
    card.locator(f'button.opt[data-k="{wrong}"]').click()
    check(card.locator("button.opt.wrong").count() == 1 and card.locator("button.opt.right").count() == 1, "a wrong pick marks both the wrong and the right option")
    check(card.locator(".rv").is_visible() and card.locator(".wn li").count() >= 1, "solution and 'why not the others' appear after answering")
    pg.screenshot(path=os.path.join(SHOTS, "qtype.png")) if SHOTS else None
    # bank
    pg.locator('#panel button[data-bank^="qtype"]').click(); pg.wait_for_timeout(500)
    check(pg.locator("#bank").is_visible() and pg.locator("#cards .qz").count() == 9, f"'Practice this type' opens the bank filtered to 9 questions ({pg.locator('#cards .qz').count()})")
    pg.click('#filters button[data-f="src"][data-v="pyq"]'); pg.wait_for_timeout(300)
    check(pg.locator("#cards .qz").count() == 4, "source filter: past questions only gives 4")
    pg.click('#filters button[data-f="level"][data-v="Easy"]'); pg.wait_for_timeout(300)
    check(pg.locator("#cards .qz").count() == 1, f"difficulty filter Easy gives 1 ({pg.locator('#cards .qz').count()})")
    pg.click("#filters [data-reset]"); pg.wait_for_timeout(300)
    n_all = int(pg.inner_text("#filters .fcount").split()[0])
    check(n_all == nbank, f"clearing filters shows all {nbank} ({n_all})")
    pg.select_option('#filters select[data-sel="sort"]', "hard"); pg.wait_for_timeout(500)
    check(pg.locator("#cards .lvl").first.inner_text() == "Hard", "sort hardest first puts a Hard question on top")
    pg.click('#filters button[data-f="lik"][data-v="high"]'); pg.wait_for_timeout(300)
    check(int(pg.inner_text("#filters .fcount").split()[0]) < nbank, "likelihood filter narrows the list")
    pg.select_option('#filters select[data-sel="tech"]', "sign-check"); pg.click("#filters [data-reset]"); pg.select_option('#filters select[data-sel="tech"]', "sign-check"); pg.wait_for_timeout(300)
    check(pg.locator("#cards .qz").count() > 0, "technique filter finds questions that use the sign check")
    c0 = pg.locator("#cards .qz").first; c0.locator("[data-reveal]").click()
    check(c0.locator(".rv").is_visible() and c0.locator("button.opt.right").count() == 1, "'Show answer' reveals without answering")
    pg.click("#filters [data-reset]"); pg.wait_for_timeout(300)
    c1 = pg.locator("#cards .qz").first; k1 = c1.get_attribute("data-key"); c1.locator(f'button.opt[data-k="{k1}"]').click()
    check("Correct" in c1.locator(".verdict").inner_text(), "right answer says Correct")
    saved = pg.evaluate("JSON.parse(localStorage.getItem('mw-progress')||'{}')")
    check(saved.get(c1.get_attribute("data-id"), {}).get("r") == 1 and len(saved) == 2, "progress (one wrong, one right) is remembered in this browser")
    pg.click("#tabs button[data-view=web]"); pg.fill("#q", "multiplier"); pg.wait_for_timeout(900)
    check("match" in pg.inner_text("#panel h2") and "0 matches" not in pg.inner_text("#panel h2"), "search finds the multiplier method across topics")
    pg.screenshot(path=os.path.join(SHOTS, "search.png")) if SHOTS else None
    pg.fill("#q", ""); pg.wait_for_timeout(300)
    pg.click("#tabs button[data-view=bank]"); pg.wait_for_timeout(500)
    if SHOTS: pg.screenshot(path=os.path.join(SHOTS, "bank.png"))
    m = page(390, 844)
    check(m.evaluate("document.documentElement.scrollWidth") <= 390, "phone: no sideways scroll on the web view")
    m.click("#tabs button[data-view=bank]"); m.wait_for_timeout(600)
    check(m.evaluate("document.documentElement.scrollWidth") <= 390, f"phone: no sideways scroll in the bank ({m.evaluate('document.documentElement.scrollWidth')})")
    if SHOTS: m.screenshot(path=os.path.join(SHOTS, "mobile_bank.png"))
    d = page(1280, 900, "dark"); d.click("#tabs button[data-view=bank]"); d.wait_for_timeout(600)
    if SHOTS: d.screenshot(path=os.path.join(SHOTS, "dark_bank.png"))
    b.close()
check(not errs, "no console errors" + (f": {errs}" if errs else ""))
print("\nFAILED: %d" % len(fails) if fails else "\nall checks passed")
sys.exit(1 if fails else 0)
