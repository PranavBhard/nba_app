Parse sites out of response and parse requests.get(<site>).content

## Best default stack (in order)

1. **trafilatura** (best “just works” on many pages)
2. **readability-lxml** (strong on article-like pages)
3. Fallback: **BeautifulSoup + light heuristics** (text density + link density)

That gives you robustness without needing Playwright.

---

## 0) Quick: normalize + parse with lxml (fast)

Use `lxml.html.fromstring` for speed and good DOM traversal; use bs4 only if you prefer it.

Key: always parse bytes with encoding detection when you can.

---

## 1) Try trafilatura first (single call)

It’s fast and usually nails “main content”.

```python
import trafilatura

def extract_trafilatura(html: str) -> str | None:
    # favor_recall=True tends to under-filter (keeps more)
    return trafilatura.extract(
        html,
        include_comments=False,
        include_tables=True,
        include_links=False,
        favor_recall=True
    )
```

If this returns a decent-length string, you’re done.

---

## 2) If that fails/thin: readability-lxml

```python
from readability import Document

def extract_readability(html: str) -> str:
    doc = Document(html)
    # doc.summary() is HTML of the extracted article
    return doc.summary()
```

Then run that returned HTML through your “HTML → structured text” converter (below).

---

## 3) Fallback: bs4 heuristic container scoring (under-filtering)

This avoids brittle selectors and drops obvious chrome (nav/footer/etc) while keeping uncertain stuff.

```python
import re
from bs4 import BeautifulSoup

JUNK_TAGS = {"script", "style", "noscript", "svg", "canvas", "iframe", "form"}
# keep this list SMALL to under-filter; add more only if you're confident
JUNK_LANDMARK_TAGS = {"nav", "footer", "header", "aside"}

JUNK_HINT_RE = re.compile(
    r"\b(nav|menu|header|footer|sidebar|cookie|banner|modal|subscribe|newsletter|promo|ad|breadcrumb)\b",
    re.I
)

PUNCT_RE = re.compile(r"[.!?,;:]")

def _link_density(el) -> float:
    text = el.get_text(" ", strip=True)
    if not text:
        return 0.0
    link_text = " ".join(a.get_text(" ", strip=True) for a in el.find_all("a"))
    return len(link_text) / max(len(text), 1)

def _score_block(el) -> float:
    text = el.get_text(" ", strip=True)
    if not text:
        return 0.0
    ld = _link_density(el)
    punct = len(PUNCT_RE.findall(text))
    # Under-filter bias: reward raw text length heavily, penalize link-dense blocks
    return len(text) * (1.0 - ld) + punct * 50

def extract_bs4_scored(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    # remove obvious junk tags
    for t in soup.find_all(list(JUNK_TAGS)):
        t.decompose()

    # remove obvious chrome landmarks (conservative)
    for t in soup.find_all(list(JUNK_LANDMARK_TAGS)):
        t.decompose()

    # remove elements whose id/class strongly suggests chrome (conservative)
    for el in soup.find_all(True):
        attrs = " ".join(filter(None, [
            el.get("id", ""),
            " ".join(el.get("class", [])) if el.get("class") else ""
        ]))
        if attrs and JUNK_HINT_RE.search(attrs):
            # don’t nuke huge containers unless you're sure:
            if el.name in {"div", "section", "aside"}:
                # keep if it’s very text-heavy (under-filter)
                if len(el.get_text(" ", strip=True)) < 400:
                    el.decompose()

    # candidates: broad set of blocks
    candidates = soup.find_all(["main", "article", "section", "div"])
    if not candidates:
        return soup.get_text("\n", strip=True)

    best = max(candidates, key=_score_block)
    return best.get_text("\n", strip=True)
```

This is surprisingly effective for “standard” pages and errs on keeping content.

---

## 4) Convert HTML to *structured* text (paragraphs, lists, headings)

Even if you use trafilatura/readability, you often want clean block formatting.

```python
from bs4 import BeautifulSoup

BLOCK_TAGS = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "pre"}

def html_to_structured_text(html_fragment: str) -> str:
    soup = BeautifulSoup(html_fragment, "lxml")

    # remove scripts/styles if any remain
    for t in soup(["script", "style", "noscript"]):
        t.decompose()

    lines = []
    for el in soup.find_all(BLOCK_TAGS):
        txt = el.get_text(" ", strip=True)
        if not txt:
            continue
        if el.name.startswith("h"):
            level = int(el.name[1])
            lines.append("\n" + "#" * level + " " + txt)
        elif el.name == "li":
            lines.append("- " + txt)
        else:
            lines.append(txt)

    out = "\n".join(lines)
    # collapse excessive blank lines
    out = re.sub(r"\n{3,}", "\n\n", out).strip()
    return out
```

Structured extraction makes later filtering MUCH easier and safer.

---

## 5) Conservative post-filter (line-based, under-filter)

Do this after you have text. Keep it conservative.

```python
import re

BOILERPLATE_RE = re.compile(
    r"(privacy|terms|cookie|all rights reserved|subscribe|newsletter|sign up|log in|copyright)",
    re.I
)

def light_cleanup(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines()]
    kept = []
    for ln in lines:
        if not ln:
            kept.append("")
            continue
        # drop extremely short boilerplate-y lines
        if len(ln) < 40 and BOILERPLATE_RE.search(ln):
            continue
        kept.append(ln)
    out = "\n".join(kept)
    out = re.sub(r"\n{3,}", "\n\n", out).strip()
    return out
```

---

## 6) One function: HTML → best-effort text (fast)

```python
def extract_main_text(html: str) -> str:
    # 1) trafilatura
    try:
        t = extract_trafilatura(html)
        if t and len(t) > 400:
            return light_cleanup(t)
    except Exception:
        pass

    # 2) readability -> structured text
    try:
        art_html = extract_readability(html)
        t = html_to_structured_text(art_html)
        if t and len(t) > 400:
            return light_cleanup(t)
    except Exception:
        pass

    # 3) bs4 fallback
    t = extract_bs4_scored(html)
    return light_cleanup(t)
```

---

## Important reality check (requests-only)

Some sites won’t work well because content is JS-rendered. Without a headless browser, your options are:

* Find their underlying JSON endpoints (best)
* Accept that extraction will be thin for those pages

A quick “is it JS rendered?” heuristic: if the extracted text is tiny but HTML is huge and contains lots of `__NEXT_DATA__`, `window.__APOLLO_STATE__`, etc., you probably need to hit an API endpoint or parse embedded JSON.
---