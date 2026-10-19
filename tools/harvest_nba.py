"""
Collect real r/nba comments for TakeMeter to label.

Two stages, kept apart on purpose:

    fetch   Pull listing pages and thread pages off a Redlib mirror and save
            the HTML untouched. Needs a browser, because the mirror runs a
            proof-of-work check before it serves anything.

    build   Turn the saved HTML into one pool of candidate comments
            (.harvest/pool.csv). Standard library only, no network, so it
            re-runs without the scraping dependency.

    python tools/harvest_nba.py fetch          # scrapling's Python
    python tools/harvest_nba.py build          # any Python 3.10+

Reddit refuses direct API calls from this machine (403), so the source is
safereddit.com, a read-only Redlib front end that serves the same threads as
plain HTML. Usernames never leave this script: the pool keeps the comment text
and the thread it came from, nothing about who wrote it.

The pool is NOT the dataset. labels.csv is: a labelled subset of this pool.
"""

from __future__ import annotations

import argparse
import csv
import html as html_lib
import json
import random
import re
import sys
import time
from pathlib import Path

MIRROR = "https://safereddit.com"
SUBREDDIT = "nba"

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / ".harvest"

def _search(query: str, window: str) -> str:
    q = query.replace(" ", "+")
    return f"/r/{SUBREDDIT}/search?q={q}&restrict_sr=on&sort=top&t={window}"


# Where threads come from. A mix on purpose: top-of-the-week threads are mostly
# clips and news, which pull reactions and jokes; Discussion and [OC] threads
# pull the stat-backed arguments. Sampling only one kind would hand the model a
# community that doesn't exist.
LISTINGS: list[tuple[str, str, int]] = [
    ("top_week", f"/r/{SUBREDDIT}/top?t=week", 3),
    ("top_month", f"/r/{SUBREDDIT}/top?t=month", 2),
    ("hot", f"/r/{SUBREDDIT}/hot", 1),
    # The mirror can't search by flair, so these are title searches that pull
    # the threads where people argue rather than react.
    ("oc", _search("OC", "month"), 1),
    ("predictions", _search("predictions", "month"), 1),
    ("mvp", _search("MVP", "month"), 1),
    ("overrated", _search("overrated", "year"), 1),
    ("unpopular", _search("unpopular opinion", "year"), 1),
]

# Threads per listing, and the comment-count window a thread has to sit in.
# Under 40 there is too little argument to sample from; over 4000 the page is a
# game thread whose comments are one-word reactions to plays nobody can see.
PER_LISTING = 10
MIN_COMMENTS, MAX_COMMENTS = 40, 4000

CHALLENGE = "Verifying your browser"


# --------------------------------------------------------------------------
# fetch
# --------------------------------------------------------------------------

def fetch_stage(delay: float) -> None:
    try:
        from scrapling.fetchers import StealthySession
    except ImportError:
        sys.exit(
            "The fetch stage needs scrapling (pip install 'scrapling[fetchers]'; "
            "scrapling install). The build stage does not."
        )

    (RAW / "listings").mkdir(parents=True, exist_ok=True)
    (RAW / "threads").mkdir(parents=True, exist_ok=True)

    with StealthySession(headless=True) as session:

        def grab(url: str) -> str:
            """One page, waiting longer each time the proof-of-work page shows."""
            # network_idle never settles on some listing pages (thumbnails keep
            # streaming), so it rode the full timeout every time. A fixed short
            # wait gets the whole server-rendered page in a few seconds.
            for wait in (2500, 6000, 15000):
                resp = session.fetch(url, network_idle=False, wait=wait, timeout=60000)
                page = _body_of(resp)
                if CHALLENGE not in page[:4000] and len(page) > 5000:
                    return page
            return ""

        seen: set[str] = set()
        queue: list[tuple[str, str]] = []

        for slug, path, pages in LISTINGS:
            url = MIRROR + path
            picked_here = 0
            for page_no in range(1, pages + 1):
                cached = RAW / "listings" / f"{slug}_p{page_no}.html"
                page = cached.read_text(encoding="utf-8") if cached.exists() else grab(url)
                if not page:
                    print(f"  listing MISS {slug} p{page_no}", flush=True)
                    break
                (RAW / "listings" / f"{slug}_p{page_no}.html").write_text(page, encoding="utf-8")
                picks = _pick_threads(page, PER_LISTING - picked_here, seen)
                queue.extend((slug, href) for href in picks)
                picked_here += len(picks)
                print(f"  listing ok   {slug} p{page_no} -> {len(picks)} threads", flush=True)
                nxt = re.search(r'href="([^"]*after=t3_[^"]+)"', page)
                if picked_here >= PER_LISTING or not nxt:
                    break
                url = MIRROR + path.split("?")[0] + html_lib.unescape(nxt.group(1))
                time.sleep(delay)
            time.sleep(delay)

        print(f"\n{len(queue)} threads queued\n")
        (RAW / "queue.json").write_text(json.dumps(queue, indent=1), encoding="utf-8")

        for index, (slug, href) in enumerate(queue, 1):
            thread_id = href.strip("/").split("/")[3]
            out = RAW / "threads" / f"{slug}__{thread_id}.html"
            if out.exists():
                continue
            page = grab(MIRROR + href)
            if not page:
                print(f"  [{index}/{len(queue)}] MISS {thread_id}", flush=True)
                continue
            out.write_text(page, encoding="utf-8")
            print(f"  [{index}/{len(queue)}] ok   {thread_id}", flush=True)
            time.sleep(delay)


def _body_of(resp) -> str:
    for attr in ("html_content", "body", "content", "text"):
        value = getattr(resp, attr, None)
        if isinstance(value, str) and len(value) > 200:
            return value
    return str(resp)


def _pick_threads(page: str, limit: int, seen: set[str]) -> list[str]:
    picked = []
    for block in page.split('<div class="post" id="')[1:]:
        href = re.search(rf'href="(/r/{SUBREDDIT}/comments/[^"]+)"', block)
        comments = re.search(r'class="post_comments" title="([\d,]+) comments?"', block)
        if not href or not comments:
            continue
        link = html_lib.unescape(href.group(1)).split("?")[0]
        count = int(comments.group(1).replace(",", ""))
        if link in seen or not (MIN_COMMENTS <= count <= MAX_COMMENTS):
            continue
        seen.add(link)
        picked.append(link)
        if len(picked) >= limit:
            break
    return picked


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------

BOT_AUTHORS = {"automoderator", "nba_mod", "remindmebot", "sneakpeekbot", "savevideo"}
DEAD = {"[deleted]", "[removed]", ""}

# This file gets committed to a public, graded repo. r/nba swears constantly
# and that stays; a slur is a different thing, and a comment carrying one is
# dropped whole rather than edited.
SLURS = re.compile(
    r"\b(retard\w*|f[a4]gg\w*|n[i1]gg\w+|tr[a4]nn(?:y|ie|ies)|sp[i1]c|ch[i1]nk|k[i1]ke)\b",
    re.I,
)

# Comment length window, in characters. Under 25 is "lmao" and "this" — real,
# but there is nothing in it for a person or a model to read a distinction off.
# Over 1200 the model truncates at 128 tokens anyway and only sees the opening.
MIN_CHARS, MAX_CHARS = 25, 1200

# Comments sampled per thread. A cap keeps one huge thread from deciding what
# the whole community sounds like.
PER_THREAD = 12


def build_stage(seed: int) -> None:
    threads_dir = RAW / "threads"
    if not threads_dir.exists():
        sys.exit(f"No raw threads at {threads_dir}. Run the fetch stage first.")

    rng = random.Random(seed)
    rows: list[dict] = []
    sources: dict[str, dict] = {}

    for path in sorted(threads_dir.glob("*.html")):
        listing, thread_id = path.stem.split("__")
        page = path.read_text(encoding="utf-8")
        title = _thread_title(page)
        comments = [c for c in _parse_comments(page) if _keep(c)]
        rng.shuffle(comments)
        for c in comments[:PER_THREAD]:
            rows.append({
                "thread_id": thread_id,
                "listing": listing,
                "score": c["score"],
                "text": c["text"],
            })
        sources[thread_id] = {"title": title, "listing": listing,
                              "url": f"https://www.reddit.com/r/{SUBREDDIT}/comments/{thread_id}/",
                              "eligible": len(comments)}

    # One shuffled order for the whole pool, fixed by the seed. Labelling walks
    # it top to bottom, so the 20 cold rows are whatever came first, not picks.
    seen: set[str] = set()
    unique = []
    for row in rows:
        key = row["text"].lower()
        if key not in seen:
            seen.add(key)
            unique.append(row)
    rng.shuffle(unique)
    for index, row in enumerate(unique, 1):
        row["pool_id"] = f"p{index:04d}"

    with (RAW / "pool.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["pool_id", "thread_id", "listing", "score", "text"])
        writer.writeheader()
        writer.writerows(unique)

    (REPO / "data").mkdir(exist_ok=True)
    (REPO / "data" / "nba_sources.json").write_text(
        json.dumps(sources, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"{len(sources)} threads, {len(unique)} candidate comments -> .harvest/pool.csv")
    print("thread list -> data/nba_sources.json")


def _thread_title(page: str) -> str:
    block = re.search(r'<h1 class="post_title">(.*?)</h1>', page, re.S)
    if not block:
        return ""
    text = re.sub(r'<a [^>]*class="post_flair".*?</a>', "", block.group(1), flags=re.S)
    return re.sub(r"\s+", " ", _strip_tags(text)).strip()


def _parse_comments(page: str) -> list[dict]:
    """Every comment on the page, in page order, one dict each."""
    starts = [m for m in re.finditer(r'<div id="([a-z0-9]+)" class="comment">', page)]
    out = []
    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(page)
        seg = page[m.start():end]
        score = re.search(r'<p class="comment_score" title="(-?\d+)"', seg)
        author = re.search(r'class="comment_author[^"]*" href="/user/([^"]+)"', seg)
        body = re.search(r'<div class="comment_body[^"]*"><div class="md">(.*?)</div></div>', seg, re.S)
        out.append({
            "id": m.group(1),
            "score": int(score.group(1)) if score else 0,
            "author": author.group(1).lower() if author else "",
            "text": _to_text(body.group(1)) if body else "",
        })
    return out


def _keep(c: dict) -> bool:
    text = c["text"]
    if c["author"] in BOT_AUTHORS or text.lower() in DEAD:
        return False
    if c["score"] < 2 or SLURS.search(text):
        return False
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        return False
    # A bare link or a gif with a caption of one word isn't a post anyone wrote.
    if len(re.sub(r"\[(link|gif)[^\]]*\]", "", text).strip()) < MIN_CHARS:
        return False
    return True


def _to_text(fragment: str) -> str:
    """Rendered markdown down to one line of plain text. Nothing is cut."""
    text = fragment
    text = re.sub(r"<(script|style)\b.*?</\1>", "", text, flags=re.S | re.I)
    # Reddit gifs and images: keep that there was one, drop the URL.
    text = re.sub(r"<img[^>]*>", " [gif] ", text, flags=re.I)
    text = re.sub(r'<a [^>]*href="[^"]*(?:giphy|\.gif)[^"]*"[^>]*>.*?</a>', " [gif] ", text, flags=re.S | re.I)
    # A link keeps its domain: "[link: basketball-reference.com]" still tells a
    # reader the poster pointed at a source, which is half of what analysis is.
    text = re.sub(
        r'<a [^>]*href="https?://(?:www\.)?([^/"]+)[^"]*"[^>]*>.*?</a>',
        lambda m: f" [link: {m.group(1)}] ",
        text, flags=re.S | re.I,
    )
    text = re.sub(r"<blockquote>(.*?)</blockquote>",
                  lambda m: ' "' + _strip_tags(m.group(1)).strip() + '" ', text, flags=re.S | re.I)
    text = re.sub(r"<li[^>]*>", " - ", text, flags=re.I)
    text = re.sub(r"<br\s*/?>|</p>|</li>|</h\d>|</tr>", " ", text, flags=re.I)
    text = _strip_tags(text)
    text = re.sub(r"https?://\S+", "[link]", text)
    # Other redditors aren't public figures. Players and reporters are.
    text = re.sub(r"\bu/[A-Za-z0-9_-]+", "u/[user]", text)
    return re.sub(r"\s+", " ", text).strip()


def _strip_tags(fragment: str) -> str:
    return html_lib.unescape(re.sub(r"<[^>]+>", "", fragment))


def main() -> None:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("stage", choices=["fetch", "build"])
    parser.add_argument("--delay", type=float, default=1.5, help="seconds between pages")
    parser.add_argument("--seed", type=int, default=2026, help="fixes the sample and its order")
    args = parser.parse_args()
    if args.stage == "fetch":
        fetch_stage(args.delay)
    else:
        build_stage(args.seed)


if __name__ == "__main__":
    main()
