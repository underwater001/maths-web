#!/usr/bin/env python3
"""Browser test of the site: loads it from a local server and clicks through the syllabus, a topic page,
mixed practice, Sources and search.

    python3 tools/render_test.py [screenshot_dir]

Needs Playwright and Chrome. The fonts are blocked (the sandbox has no network), which is expected and ignored.
"""
import http.server, json, os, socketserver, sys, threading
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = sys.argv[1] if len(sys.argv) > 1 else None
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
    if "fonts.g" in u: r.abort()
    else:
        reqs.append(u); r.continue_()


def shard(t): return json.load(open(os.path.join(ROOT, "data", "shards", t + ".json"), encoding="utf-8"))


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])

    def page(w, h, scheme="light", hash_=""):
        c = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme); pg = c.new_page()
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "ERR_" not in m.text and "fonts" not in m.text else None)
        pg.on("pageerror", lambda e: errs.append("PAGEERROR " + str(e)))
        pg.route("**/*", route); pg.goto(f"http://127.0.0.1:{port}/index.html{hash_}")
        pg.wait_for_selector(".tcard, #topic .sect", timeout=15000); pg.wait_for_timeout(500); return pg

    core = json.load(open(os.path.join(ROOT, "data", "core.json")))
    nbank = len(core["bank"]["rows"])
    PL = shard("profit-loss")
    n_topics = len([n for n in core["nodes"].values() if n.get("kind") == "topic"])
    n_subjects = len([n for n in core["nodes"].values() if n.get("parent") == "hub" and n.get("kind") != "topic"])
    built = [t for t, m in core["topics"].items() if m.get("built")]
    pl_rows = [r for r in core["bank"]["rows"] if r[1] == "profit-loss"]
    pl_types = [n for n, v in core["nodes"].items() if v.get("kind") == "qtype" and v.get("parent", "").startswith("c-pl-")]

    # ---------------- the syllabus ----------------
    pg = page(1280, 1000)
    check(not any("/shards/" in u for u in reqs), "the syllabus loads no topic shard (nothing fetched until a topic is opened)")
    check(not any("d3" in u.lower() for u in reqs), "no charting library is loaded at all")
    check(pg.locator(".tcard").count() == n_topics, f"every one of the {n_topics} topics has a card")
    check(pg.locator(".subject").count() == n_subjects, f"topics are grouped under the {n_subjects} subjects")
    check(pg.locator("#syllabus .chip[data-type]").count() >= 5, "the most-asked question types are offered up front")
    check(pg.locator(".tcard.todo").count() == n_topics - len(built), "topics with no page yet are shown but dimmed")
    if SHOTS: pg.screenshot(path=os.path.join(SHOTS, "syllabus.png"))

    # ---------------- a topic page ----------------
    pg.locator('.tcard[data-topic="profit-loss"]').click(); pg.wait_for_timeout(900)
    check(pg.locator("#topic").is_visible() and "Profit" in pg.inner_text("#topic h2"), "clicking a topic opens its page")
    check("#t/profit-loss" in pg.evaluate("location.hash"), "the topic page has its own link")
    check(any("shards/profit-loss" in u for u in reqs) and not any("shards/partnership" in u for u in reqs), "it loads only that topic's data")
    # study first
    study = pg.inner_text("#study")
    check(pg.locator("#study .card").count() >= 4, "study section: one card per concept")
    check(pg.locator("#study .formula").count() == len(PL["formulas"]), f"all {len(PL['formulas'])} formulas are on the page")
    check("Tricks that save time" in study and "Traps to avoid" in study, "tricks and traps are collected at the top, before the questions")
    # then the types, each with its pattern
    types_txt = pg.inner_text("#types")
    check(pg.locator("#types .card").count() == len(pl_types), f"a card for each of the {len(pl_types)} question types")
    check(pg.locator("#types .pattern").count() == len(pl_types), "every type states the pattern that identifies it")
    check(PL["methods"]["q-pl-chain"]["cue"] in types_txt, "the pattern is the type's own cue")
    check(pg.locator("#types details.more").count() == len(pl_types), "the full method, formulas and traps sit behind one tap")
    # then the questions
    check(pg.locator("#questions").evaluate("e => e.getBoundingClientRect().top") > pg.locator("#study").evaluate("e => e.getBoundingClientRect().top"),
          "questions come after the study material, not before")
    check(pg.locator("#topic .q").count() == 20, "questions load 20 at a time")
    first = pg.locator("#topic .q").first
    check("Easy" in first.inner_text(), "easiest question first")
    tags = first.locator(".tags").first.inner_text()
    check("repeats:" in tags and "asked 12 Sep 2025" in tags, "each question is tagged with how often it repeats and when it was asked")
    check(first.locator(".rv").is_hidden(), "the answer stays hidden until you try")
    if SHOTS: pg.screenshot(path=os.path.join(SHOTS, "topic.png"))

    # answering
    key = first.get_attribute("data-key")
    wrong = [k for k in "abcd" if k != key][0]
    first.locator(f'button.opt[data-k="{wrong}"]').click(); pg.wait_for_timeout(300)
    check(first.locator("button.opt.wrong").count() == 1 and first.locator("button.opt.right").count() == 1, "a wrong pick marks both options")
    rv = first.locator(".rv").inner_text()
    check(all(w in rv for w in ["SOLUTION", "WHY NOT THE OTHERS", "TRAPS IN THIS TYPE"]), "the answer carries the solution, the eliminations and the traps")
    saved = pg.evaluate("JSON.parse(localStorage.getItem('mw-progress')||'{}')")
    check(len(saved) == 1, "the answer is remembered")

    # filter the questions down to one type
    pg.locator('#questions .chip[data-only="q-pl-weight"]').click(); pg.wait_for_timeout(400)
    n_weight = len([x for x in PL["pyqs"] + PL["practice"] if x["qtype"] == "q-pl-weight"])
    check(pg.locator("#topic .q").count() == min(20, n_weight), f"the type filter narrows the list to its {n_weight} questions")
    pg.locator('#questions .chip[data-only=""]').click(); pg.wait_for_timeout(400)
    check(pg.locator("#topic .q").count() == 20, "and back to all types")
    pg.click("#topic [data-moreq]"); pg.wait_for_timeout(400)
    check(pg.locator("#topic .q").count() == 40, "'show more' adds the next 20")

    # a type link from the syllabus lands on that type
    pg.click("#topic [data-home]"); pg.wait_for_timeout(400)
    pg.locator('.tcard[data-topic="profit-loss"] [data-type]').first.click(); pg.wait_for_timeout(800)
    check(pg.evaluate("location.hash").startswith("#t/profit-loss/"), "a question type on a card opens the topic at that type")

    # a topic with no page yet says so
    pg.goto(f"http://127.0.0.1:{port}/index.html#t/statistics"); pg.wait_for_timeout(700)
    check("not built yet" in pg.inner_text("#topic").lower(), "a topic with no page yet explains itself instead of breaking")

    # a quiz-tier topic (past questions, no extra practice) works the same way
    pg.goto(f"http://127.0.0.1:{port}/index.html#t/average"); pg.wait_for_timeout(900)
    AV = shard("average")
    check(pg.locator("#study .card").count() >= 3 and pg.locator("#types .pattern").count() >= 1, "a quiz-tier topic still has concepts and patterns")
    while pg.locator("#topic .q").count() < len(AV["pyqs"]) and pg.locator("#topic [data-moreq]").count() > 0:
        pg.click("#topic [data-moreq]"); pg.wait_for_timeout(400)
    check(pg.locator("#topic .q").count() == len(AV["pyqs"]), f"all {len(AV['pyqs'])} of its questions are there")
    check("ULTRA-CALC" not in pg.inner_text("#types"), "no empty ultra-calc line where a topic has none")

    # ---------------- mixed practice ----------------
    pg.click('#tabs [data-view="practice"]'); pg.wait_for_timeout(900)
    check(int(pg.inner_text("#filters .fcount").split()[0]) == nbank, f"mixed practice starts with all {nbank} questions")
    pg.click('#filters [data-f="src"][data-v="pyq"]'); pg.wait_for_timeout(600)
    n_pyq = len([r for r in core["bank"]["rows"] if r[4] == "pyq"])
    check(int(pg.inner_text("#filters .fcount").split()[0]) == n_pyq, f"the source filter gives the {n_pyq} past questions")
    pg.click("#filters [data-reset]"); pg.wait_for_timeout(600)
    pg.select_option('#filters [data-sel="sort"]', "hard"); pg.wait_for_timeout(700)
    check("Hard" in pg.locator("#cards .q").first.inner_text(), "sorting hardest first puts a Hard question on top")
    c0 = pg.locator("#cards .q").first
    c0.locator("[data-reveal]").click(); pg.wait_for_timeout(300)
    check(c0.locator(".rv").is_visible() and c0.locator("button.opt.right").count() == 1, "'show the answer' reveals it without guessing")
    if SHOTS: pg.screenshot(path=os.path.join(SHOTS, "practice.png"))

    # ---------------- sources ----------------
    pg.click('#tabs [data-view="sources"]'); pg.wait_for_timeout(600)
    check(pg.locator("#sources .pcard[data-pid]").count() == len(core["papers"]), f"Sources lists all {len(core['papers'])} papers")
    hrefs = pg.eval_on_selector_all("#sources .pcard[data-pid] a.ext", "els => els.map(e => e.getAttribute('href'))")
    check(sorted(hrefs) == sorted(p["link"] for p in core["papers"] if p.get("link")), "each paper shows its own source link on Sources")
    check(pg.locator("#topic a[href]").count() == 0, "topic pages carry no links to papers")
    pg.click("#sources [data-plist]"); pg.wait_for_timeout(700)
    check(pg.locator("#sources table.plist tbody tr").count() > 10, "a paper's question list opens")

    # ---------------- search ----------------
    pg.fill("#q", "discount"); pg.wait_for_timeout(1200)
    check(pg.locator("#searchres").is_visible() and "match" in pg.inner_text("#searchres h2"), "search shows what it found")
    check(pg.locator("#searchres .chip[data-topic], #searchres .chip[data-type]").count() > 0, "search offers the topics and types it matched")
    pg.locator("#searchres .chip[data-topic]").first.click(); pg.wait_for_timeout(900)
    check(pg.locator("#topic").is_visible(), "a search result opens the topic page")

    # old links still work
    pg.goto(f"http://127.0.0.1:{port}/index.html#learn-partnership"); pg.wait_for_timeout(900)
    check("Partnership" in pg.inner_text("#topic h2"), "links from the old version still land on the right topic")

    # ---------------- phone ----------------
    m = page(390, 844)
    check(m.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"), "phone: the syllabus does not scroll sideways")
    m.locator('.tcard[data-topic="profit-loss"]').click(); m.wait_for_timeout(1000)
    check(m.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"), "phone: a topic page does not scroll sideways")
    check(m.locator("#study .formula").count() > 0 and m.locator("#topic .q").count() > 0, "phone: the study material and the questions are both there")
    if SHOTS: m.screenshot(path=os.path.join(SHOTS, "mobile_topic.png"))
    m.click('#tabs [data-view="practice"]'); m.wait_for_timeout(900)
    check(m.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"), "phone: mixed practice does not scroll sideways")

    # dark
    d = page(1280, 900, "dark", "#t/profit-loss")
    d.wait_for_timeout(600)
    check(d.evaluate("getComputedStyle(document.body).backgroundColor") == "rgb(14, 19, 26)", "dark mode paints its own background")
    if SHOTS: d.screenshot(path=os.path.join(SHOTS, "dark_topic.png"))

    check(not errs, f"no console errors ({errs[:3]})")
    b.close()

srv.shutdown()
print()
if fails:
    print(f"FAILED: {len(fails)}")
    for f in fails: print(" -", f)
    sys.exit(1)
print("all checks passed")
