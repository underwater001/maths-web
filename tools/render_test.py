#!/usr/bin/env python3
"""Browser test of the site: loads it from a local server and clicks through the web, Learn, the bank, Sources and search.

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


def shard(t): return json.load(open(os.path.join(ROOT, "data", "shards", t + ".json"), encoding="utf-8"))


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
    def page(w, h, scheme="light", hash_=""):
        c = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme); pg = c.new_page()
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "ERR_FAILED" not in m.text and "fonts" not in m.text else None)
        pg.on("pageerror", lambda e: errs.append("PAGEERROR " + str(e)))
        pg.route("**/*", route); pg.goto(f"http://127.0.0.1:{port}/index.html{hash_}")
        pg.wait_for_selector(".nd", state="attached", timeout=15000); pg.wait_for_timeout(600); return pg
    core = json.load(open(os.path.join(ROOT, "data", "core.json")))
    nbank = len(core["bank"]["rows"]); PL = shard("profit-loss"); PT = shard("partnership")
    pl_rows = [r for r in core["bank"]["rows"] if r[1] == "profit-loss"]
    chain_n = len([x for x in PL["pyqs"] if x["qtype"] == "q-pl-chain"]) + len([x for x in PL["practice"] if x["qtype"] == "q-pl-chain"])
    mult_formulas = len([f for f in PL["formulas"] if f["node"] == "c-pl-multiplier"])

    # ---------------- web ----------------
    pg = page(1280, 900)
    check(not any("/shards/" in u for u in reqs), "start-up fetches no topic shard (lazy loading)")
    check(f"{nbank} questions in the bank" in pg.inner_text("#panel h2"), f"overview says {nbank} questions in the bank")
    check(pg.locator(".ring").count() >= 9, f"built nodes are ringed ({pg.locator('.ring').count()})")
    pg.locator('.nd[data-id="profit-loss"]').click(); pg.wait_for_timeout(300)
    panel = pg.inner_text("#panel")
    check("This topic" in panel and "of 3 shifts" in panel, "topic panel shows how often it was asked")
    check(pg.locator("#panel .qz").count() == 0 and pg.locator("#panel .formula").count() == 0, "side panel is slim: no question cards or formula lists")
    check(pg.locator("#panel a[href]").count() == 0, "side panel has no links to papers")
    check(pg.locator('#panel [data-learn^="start:"]').count() == 1, "topic panel has 'Start learning'")
    check(not any("shards/" in u for u in reqs), "browsing the web panel fetches no shard")

    # ---------------- end node -> Learn at the first concept ----------------
    pg.locator('.nd[data-id="q-pl-chain"]').click(); pg.wait_for_selector("#lmain h2"); pg.wait_for_timeout(300)
    check(pg.locator("#learn").is_visible() and not pg.locator(".layout").is_visible(), "clicking an end node opens the topic's Learn view")
    check(any("shards/profit-loss" in u for u in reqs) and not any("shards/partnership" in u for u in reqs), "Learn fetches only that topic's shard")
    check("Concept 1 of 4" in pg.locator("#lmain").text_content(), "it starts at the first concept")
    check(pg.locator("#lmain .formula").count() == mult_formulas, f"first concept lists its {mult_formulas} formulas")
    check(pg.locator("#lmain .banner").count() == 1 and "Skip to that type" in pg.locator("#lmain .banner").text_content(), "banner offers a jump to the type that was clicked")
    check(pg.locator("#lmain a[href]").count() == 0 and pg.locator("#learn a[href]").count() == 0, "Learn shows no links to papers")
    pg.screenshot(path=os.path.join(SHOTS, "learn_concept.png")) if SHOTS else None
    # walk every step up to the quiz
    n_steps = pg.locator("#outline button.oi").count()
    check(n_steps == 1 + 4 + 5 + 1, f"outline: overview + 4 concepts + 5 types + quiz ({n_steps})")
    pg.click("#lmain [data-next]"); pg.wait_for_timeout(200)
    t = pg.locator("#lmain").text_content(); m = PL["methods"]["q-pl-chain"]
    check("Concept 1 · type 1 of 1" in t and m["cue"] in t, "next step is the type, with its cue")
    check(pg.locator("#lmain .capsule > div").count() == 3, "capsule: spot it, do this, watch out")
    lab = pg.locator("#lmain dl.ledger dt").all_text_contents()
    check(all(x in lab for x in ["Standard", "Fast", "Ultra-calc", "Eliminate", "Traps", "Variations"]), f"method layers all shown ({lab})")
    pg.screenshot(path=os.path.join(SHOTS, "learn_type.png")) if SHOTS else None
    steps = 3
    while pg.locator("#lmain [data-next]").count():
        label = pg.inner_text("#lmain [data-next]"); pg.click("#lmain [data-next]"); pg.wait_for_timeout(60); steps += 1
    check(steps == n_steps and "Start the quiz" in label, f"Next walks all {n_steps} steps and ends with 'Start the quiz'")
    check("quiz" in pg.locator("#lmain h2").text_content() and f"Start all {len(pl_rows)} questions" in pg.locator("#lmain").text_content(), f"quiz menu offers all {len(pl_rows)} questions")

    # ---------------- the quiz ----------------
    pg.click("#lmain [data-qs=all]"); pg.wait_for_timeout(200)
    check(f"Question 1 of {len(pl_rows)}" in pg.locator("#lmain").text_content(), "quiz starts at question 1")
    check(pg.locator("#lmain [data-qnext]").is_disabled(), "Next question is locked until you answer")
    key = pg.locator("#lmain .lq").get_attribute("data-id")
    x = next(v for v in PL["pyqs"] + PL["practice"] if v["id"] == key)
    wrong = [k for k in "abcd" if k != x["key"]][0]
    pg.click(f'#lmain button.opt[data-k="{wrong}"]'); pg.wait_for_timeout(100)
    rv = pg.locator("#lmain .rv").text_content()
    check(pg.locator("#lmain button.opt.wrong").count() == 1 and pg.locator("#lmain button.opt.right").count() == 1, "a wrong pick marks both options")
    check(all(w in rv for w in ["Solution", "Why not the others", "Eliminate using the options", "Traps in this type"]), "answer shows solution, eliminations, why-not and traps")
    check(not pg.locator("#lmain [data-qnext]").is_disabled(), "answering unlocks Next")
    pg.screenshot(path=os.path.join(SHOTS, "learn_quiz.png")) if SHOTS else None
    # play every question by keyboard, recording the order of phases per type
    seq = []
    for i in range(len(pl_rows)):
        ph = pg.locator("#lmain .qhead").first.inner_text().split("\n"); seq.append(" ".join(ph))
        if i: pg.keyboard.press("b") if False else None
        if pg.locator("#lmain .rv").count() == 0: pg.keyboard.press("a")
        pg.keyboard.press("Enter"); pg.wait_for_timeout(30)
    check("Result" in pg.locator("#lmain").text_content(), "finishing shows the result")
    order = {"Past question": 0, "Practice": 1, "Challenge": 2}
    phases, ok = [], True
    for sline in seq:
        for k, v in order.items():
            if k in sline: phases.append(v)
    check(len(phases) == len(pl_rows), "every quiz question carries a phase label")
    # within each type, phases never go backwards
    types = [x["qtype"] for t_ in [t_ for t_ in []] for x in []]
    ordered = [e for q in ["q-pl-chain", "q-pl-weight", "q-pl-free", "q-pl-rate", "q-pl-equal"] for e in
               ([0] * len([x for x in PL["pyqs"] if x["qtype"] == q]) + [1] * len([x for x in PL["practice"] if x["qtype"] == q and x["variant"] != "harder"]) + [2] * len([x for x in PL["practice"] if x["qtype"] == q and x["variant"] == "harder"]))]
    check(phases == ordered, "quiz order per type: past questions, then same-level practice, then harder")
    check(pg.locator("#lmain .rows li").count() == 5 and pg.locator("#lmain [data-qs=wrong]").count() == 1, "result lists the 5 types and offers 'Redo wrong answers'")
    pg.screenshot(path=os.path.join(SHOTS, "learn_result.png")) if SHOTS else None
    saved = pg.evaluate("JSON.parse(localStorage.getItem('mw-progress')||'{}')")
    check(len(saved) == len(pl_rows), f"progress for all {len(pl_rows)} answers is remembered")
    mem = pg.evaluate("JSON.parse(localStorage.getItem('mw-learn')||'{}')")
    check(mem.get("profit-loss", {}).get("i") == n_steps - 1, "the last step is remembered for 'Continue'")
    nwrong = sum(1 for v in saved.values() if v["r"] == 0)
    pg.click("#lmain [data-qs=wrong]"); pg.wait_for_timeout(200)
    check(f"Question 1 of {nwrong}" in pg.locator("#lmain").text_content(), f"'Redo wrong answers' replays exactly the {nwrong} wrong ones")
    # a single type from the type page
    pg.click("#outline button.oi >> text=Markup"); pg.wait_for_timeout(200)
    pg.click("#lmain [data-qs=q-pl-chain]"); pg.wait_for_timeout(200)
    check(f"Question 1 of {chain_n}" in pg.locator("#lmain").text_content(), f"'Quiz on this type' runs the type's {chain_n} questions")

    # ---------------- question bank ----------------
    pg.click("#tabs button[data-view=bank]"); pg.wait_for_timeout(300)
    check(pg.locator("#bytopic .tcard").count() == 2, "bank by topic shows the 2 built topics")
    check(pg.locator("#bytopic .tcard [data-learn^='resume:']").count() == 1 and pg.locator("#bytopic .tcard [data-learn^='start:']").count() == 2, "a started topic offers Continue and Start over")
    check("Keeps going wrong" in pg.inner_text("#bytopic"), "topic card names the methods that keep going wrong")
    check(pg.locator("#bytopic a[href]").count() == 0, "topic cards carry no links to papers")
    if SHOTS: pg.screenshot(path=os.path.join(SHOTS, "bank_topics.png"))
    pg.click("#bytopic [data-learn^='start:partnership']"); pg.wait_for_selector("#lmain h2"); pg.wait_for_timeout(200)
    check("Topic" in pg.locator("#lmain").text_content() and pg.locator("#lmain .tile").count() == 6, "'Start learning' opens the topic overview")
    pg.click("#tabs button[data-view=bank]"); pg.click("#btabs button[data-bt=mixed]"); pg.wait_for_timeout(500)
    check(pg.locator("#mixed").is_visible() and int(pg.inner_text("#filters .fcount").split()[0]) == nbank, f"mixed practice lists all {nbank}")
    check(pg.locator("#cards a[href]").count() == 0 and pg.locator("#cards .src").count() > 0, "cards show where a question came from as plain text, without links")
    pg.click('#filters button[data-f="src"][data-v="pyq"]'); pg.wait_for_timeout(300)
    n_pyq = len([r for r in core["bank"]["rows"] if r[4] == "pyq"])
    check(int(pg.inner_text("#filters .fcount").split()[0]) == n_pyq, f"source filter: past questions only gives {n_pyq}")
    pg.click("#filters [data-reset]"); pg.select_option('#filters select[data-sel="sort"]', "hard"); pg.wait_for_timeout(500)
    check(pg.locator("#cards .lvl").first.inner_text() == "Hard", "sort hardest first puts a Hard question on top")
    pg.click('#filters button[data-f="lik"][data-v="high"]'); pg.wait_for_timeout(300)
    check(int(pg.inner_text("#filters .fcount").split()[0]) < nbank, "likelihood filter narrows the list")
    pg.click("#filters [data-reset]"); pg.select_option('#filters select[data-sel="tech"]', "sign-check"); pg.wait_for_timeout(300)
    check(pg.locator("#cards .qz").count() > 0, "technique filter finds questions that use the sign check")
    c0 = pg.locator("#cards .qz").first; c0.locator("[data-reveal]").click()
    check(c0.locator(".rv").is_visible() and c0.locator("button.opt.right").count() == 1, "'Show answer' reveals without answering")
    c0.locator("[data-learn]").first.click(); pg.wait_for_selector("#lmain h2"); pg.wait_for_timeout(200)
    check("type 1 of" in pg.locator("#lmain").text_content() or "Concept 1 of" in pg.locator("#lmain").text_content(), "a card's 'Learn this type' link opens Learn")

    # ---------------- sources ----------------
    pg.click("#tabs button[data-view=sources]"); pg.wait_for_timeout(300)
    check(pg.locator("#sources .pcard[data-pid]").count() == len(core["papers"]), f"Sources lists all {len(core['papers'])} papers")
    check(pg.locator('#sources a.ext[href*="drive.google.com"]').count() == len(core["papers"]), "each paper has its link, and only here")
    check(pg.locator('#sources a.ext[href^="http"]').count() == len(core["papers"]) + len(core["refs"]), "outside reading links are listed too")
    pg.locator("#sources [data-plist]").first.click(); pg.wait_for_timeout(500)
    check(pg.locator("#sources table.plist tbody tr").count() == core["papers"][0]["n"] or pg.locator("#sources table.plist tbody tr").count() == 25, "the question list of a paper opens")
    if SHOTS: pg.screenshot(path=os.path.join(SHOTS, "sources.png"), full_page=True)

    # ---------------- search ----------------
    pg.click("#tabs button[data-view=web]"); pg.fill("#q", "multiplier"); pg.wait_for_timeout(900)
    check("match" in pg.inner_text("#panel h2") and "0 matches" not in pg.inner_text("#panel h2"), "search finds the multiplier method across topics")
    check(pg.locator("#panel a[href]").count() == 0 and pg.locator("#panel .qz").count() == 0, "search results have no links and no question cards")
    pg.fill("#q", ""); pg.wait_for_timeout(300)

    # ---------------- deep links ----------------
    h = page(1280, 900, hash_="#learn-partnership")
    check(h.locator("#learn").is_visible() and "Partnership" in h.locator("#lhead").text_content(), "#learn-<topic> opens that topic directly")
    s2 = page(1280, 900, hash_="#sources")
    check(s2.locator("#sources").is_visible(), "#sources opens the Sources page")

    # ---------------- phone and dark ----------------
    m = page(390, 844)
    W = lambda: m.evaluate("document.documentElement.scrollWidth")
    check(W() <= 390, "phone: no sideways scroll on the web view")
    m.click("#tabs button[data-view=bank]"); m.wait_for_timeout(500)
    check(W() <= 390, f"phone: no sideways scroll in the bank ({W()})")
    if SHOTS: m.screenshot(path=os.path.join(SHOTS, "mobile_bank.png"))
    m.click("#bytopic [data-learn^='start:profit-loss']"); m.wait_for_selector("#lmain h2"); m.wait_for_timeout(300)
    check(W() <= 390, f"phone: no sideways scroll in Learn ({W()})")
    check(not m.locator("#outline").is_visible(), "phone: the outline is folded away")
    m.click("#otoggle"); m.wait_for_timeout(100)
    check(m.locator("#outline").is_visible(), "phone: the outline button opens it")
    m.click("#outline button.oi >> nth=1"); m.wait_for_timeout(200)
    check("Concept 1 of" in m.locator("#lmain").text_content() and not m.locator("#outline").is_visible(), "phone: picking a step closes the outline")
    m.click("#outline button.oi >> nth=0") if m.locator("#outline").is_visible() else None
    for _ in range(9): m.click("#lmain [data-next]"); m.wait_for_timeout(40)
    m.click("#lmain [data-qs=all]"); m.wait_for_timeout(200); m.click("#lmain button.opt >> nth=0"); m.wait_for_timeout(150)
    check(W() <= 390, f"phone: no sideways scroll in a quiz question ({W()})")
    if SHOTS: m.screenshot(path=os.path.join(SHOTS, "mobile_quiz.png"))
    m.click("#tabs button[data-view=sources]"); m.wait_for_timeout(300)
    check(W() <= 390, f"phone: no sideways scroll on Sources ({W()})")
    d = page(1280, 900, "dark", "#learn-profit-loss"); d.wait_for_timeout(300)
    if SHOTS: d.screenshot(path=os.path.join(SHOTS, "dark_learn.png"))
    b.close()
check(not errs, "no console errors" + (f": {errs}" if errs else ""))
print("\nFAILED: %d" % len(fails) if fails else "\nall checks passed")
sys.exit(1 if fails else 0)
