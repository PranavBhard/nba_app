"""
Webpage Parser Service.

Extracts clean, structured text from HTML content using a waterfall approach:
1. trafilatura (best general-purpose extractor)
2. readability-lxml (strong on article-like pages)
3. BeautifulSoup + heuristics (fallback)
"""

import re
import requests
from bs4 import BeautifulSoup

try:
    import trafilatura
    HAS_TRAFILATURA = True
except ImportError:
    HAS_TRAFILATURA = False

try:
    from readability import Document
    HAS_READABILITY = True
except ImportError:
    HAS_READABILITY = False


# Constants for BS4 fallback extraction
JUNK_TAGS = {"script", "style", "noscript", "svg", "canvas", "iframe", "form"}
JUNK_LANDMARK_TAGS = {"nav", "footer", "header", "aside"}

JUNK_HINT_RE = re.compile(
    r"\b(nav|menu|header|footer|sidebar|cookie|banner|modal|subscribe|newsletter|promo|ad|breadcrumb)\b",
    re.I
)

PUNCT_RE = re.compile(r"[.!?,;:]")

BOILERPLATE_RE = re.compile(
    r"(privacy|terms|cookie|all rights reserved|subscribe|newsletter|sign up|log in|copyright)",
    re.I
)

BLOCK_TAGS = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "pre"}

# Minimum content length threshold before falling through to next method
MIN_CONTENT_LENGTH = 400


class WebpageParser:
    """Service for extracting clean text from HTML/URLs."""

    @staticmethod
    def extract_from_url(url: str, timeout: int = 10) -> str:
        """
        Fetch URL and extract main text content.

        Args:
            url: The URL to fetch and parse
            timeout: Request timeout in seconds (default 10)

        Returns:
            Extracted text content from the page

        Raises:
            requests.RequestException: If the URL fetch fails
        """
        response = requests.get(
            url,
            timeout=timeout,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
        )
        response.raise_for_status()

        # Try to decode with detected encoding, fallback to utf-8
        if response.encoding:
            html = response.text
        else:
            html = response.content.decode("utf-8", errors="replace")

        return WebpageParser.extract_from_html(html)

    @staticmethod
    def extract_from_html(html: str) -> str:
        """
        Extract main text content from HTML string.

        Uses a waterfall approach:
        1. trafilatura (if available and returns sufficient content)
        2. readability-lxml (if available and returns sufficient content)
        3. BeautifulSoup scored extraction (fallback)

        Args:
            html: Raw HTML content

        Returns:
            Extracted and cleaned text content
        """
        # 1) Try trafilatura first
        if HAS_TRAFILATURA:
            try:
                text = WebpageParser._extract_trafilatura(html)
                if text and len(text) > MIN_CONTENT_LENGTH:
                    return WebpageParser._light_cleanup(text)
            except Exception:
                pass

        # 2) Try readability -> structured text
        if HAS_READABILITY:
            try:
                article_html = WebpageParser._extract_readability(html)
                if article_html:
                    text = WebpageParser._html_to_structured_text(article_html)
                    if text and len(text) > MIN_CONTENT_LENGTH:
                        return WebpageParser._light_cleanup(text)
            except Exception:
                pass

        # 3) BS4 fallback
        text = WebpageParser._extract_bs4_scored(html)
        return WebpageParser._light_cleanup(text)

    @staticmethod
    def _extract_trafilatura(html: str) -> str | None:
        """
        Extract main content using trafilatura.

        Args:
            html: Raw HTML content

        Returns:
            Extracted text or None if extraction fails
        """
        return trafilatura.extract(
            html,
            include_comments=False,
            include_tables=True,
            include_links=False,
            favor_recall=True
        )

    @staticmethod
    def _extract_readability(html: str) -> str | None:
        """
        Extract article content using readability-lxml.

        Args:
            html: Raw HTML content

        Returns:
            HTML fragment of the extracted article
        """
        doc = Document(html)
        return doc.summary()

    @staticmethod
    def _extract_bs4_scored(html: str) -> str:
        """
        Extract content using BeautifulSoup with block scoring heuristics.

        This fallback method:
        - Removes obvious junk tags (script, style, etc.)
        - Removes chrome landmarks (nav, footer, header, aside)
        - Scores remaining blocks by text density and link density
        - Returns the highest-scoring block's text

        Args:
            html: Raw HTML content

        Returns:
            Extracted text content
        """
        soup = BeautifulSoup(html, "lxml")

        # Remove obvious junk tags
        for tag in soup.find_all(list(JUNK_TAGS)):
            tag.decompose()

        # Remove obvious chrome landmarks (conservative)
        for tag in soup.find_all(list(JUNK_LANDMARK_TAGS)):
            tag.decompose()

        # Remove elements whose id/class strongly suggests chrome (conservative)
        for el in soup.find_all(True):
            attrs = " ".join(filter(None, [
                el.get("id", ""),
                " ".join(el.get("class", [])) if el.get("class") else ""
            ]))
            if attrs and JUNK_HINT_RE.search(attrs):
                # Don't nuke huge containers unless confident
                if el.name in {"div", "section", "aside"}:
                    # Keep if it's very text-heavy (under-filter)
                    if len(el.get_text(" ", strip=True)) < 400:
                        el.decompose()

        # Candidates: broad set of blocks
        candidates = soup.find_all(["main", "article", "section", "div"])
        if not candidates:
            return soup.get_text("\n", strip=True)

        best = max(candidates, key=WebpageParser._score_block)
        return best.get_text("\n", strip=True)

    @staticmethod
    def _html_to_structured_text(html_fragment: str) -> str:
        """
        Convert HTML fragment to structured text with markdown-style formatting.

        - Headings become # H1, ## H2, etc.
        - List items become bullet points
        - Paragraphs are separated by newlines

        Args:
            html_fragment: HTML content to convert

        Returns:
            Structured text with markdown-style formatting
        """
        soup = BeautifulSoup(html_fragment, "lxml")

        # Remove scripts/styles if any remain
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

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
        # Collapse excessive blank lines
        out = re.sub(r"\n{3,}", "\n\n", out).strip()
        return out

    @staticmethod
    def _light_cleanup(text: str) -> str:
        """
        Conservative post-filter to remove common boilerplate.

        Only removes short lines that match boilerplate patterns.
        Designed to under-filter (keep uncertain content).

        Args:
            text: Text to clean

        Returns:
            Cleaned text
        """
        lines = [ln.strip() for ln in text.splitlines()]
        kept = []
        for ln in lines:
            if not ln:
                kept.append("")
                continue
            # Drop extremely short boilerplate-y lines
            if len(ln) < 40 and BOILERPLATE_RE.search(ln):
                continue
            kept.append(ln)

        out = "\n".join(kept)
        out = re.sub(r"\n{3,}", "\n\n", out).strip()
        return out

    @staticmethod
    def _link_density(el) -> float:
        """
        Calculate the ratio of link text to total text in an element.

        Args:
            el: BeautifulSoup element

        Returns:
            Float between 0 and 1 representing link density
        """
        text = el.get_text(" ", strip=True)
        if not text:
            return 0.0
        link_text = " ".join(a.get_text(" ", strip=True) for a in el.find_all("a"))
        return len(link_text) / max(len(text), 1)

    @staticmethod
    def _score_block(el) -> float:
        """
        Score a block element for content quality.

        Higher scores indicate more likely main content:
        - Rewards raw text length
        - Penalizes link-dense blocks
        - Rewards punctuation (indicates prose)

        Args:
            el: BeautifulSoup element

        Returns:
            Numeric score (higher = better content candidate)
        """
        text = el.get_text(" ", strip=True)
        if not text:
            return 0.0
        ld = WebpageParser._link_density(el)
        punct = len(PUNCT_RE.findall(text))
        # Under-filter bias: reward raw text length heavily, penalize link-dense blocks
        return len(text) * (1.0 - ld) + punct * 50
