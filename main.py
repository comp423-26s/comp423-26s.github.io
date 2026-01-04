"""MkDocs macros for COMP423 course site.

This module is loaded by mkdocs-macros-plugin during the site build. It
registers Jinja/Markdown macros and filters used across the documentation.

Primary features:

- `get_recent_and_upcoming`: Collects pages that declare a `date` in metadata
    (YAML front matter or simple `key: value` headers), filters to recent and
    upcoming entries, and returns a small structured list for display.
- `format_threads`: Formats a list of thread/tag labels for rendering.
"""

from __future__ import annotations

import datetime
import os
import re
from pathlib import Path
from typing import Any, Iterable, TypedDict, cast

from markupsafe import Markup, escape

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


class RecentItem(TypedDict):
    """Structured return type for `get_recent_and_upcoming`."""

    title: str
    url: str
    date: datetime.date
    type: str
    code: str
    threads: list[str]
    due: datetime.date | None
    delta: int


def define_env(env: Any) -> None:
    """Register macros and filters for mkdocs-macros-plugin.

    MkDocs Macros Plugin calls `define_env(env)` at build time. Anything
    decorated with `@env.macro` or `@env.filter` becomes available in templates
    and Markdown.

    Args:
        env: The macros plugin environment.
    """

    @env.macro
    def get_recent_and_upcoming(limit: int = 0) -> list[RecentItem]:
        """Get pages with dates that are recent or upcoming.

        We scan the site's pages for a `date` metadata field, keep pages whose
        date is within the last N days or in the future, and return them sorted
        by date.

        Args:
            limit: Maximum number of items to return. If falsy or non-positive,
                returns all matching items.

        Returns:
            A list of dicts with keys: `title`, `url`, `date`, `type`, `threads`,
            and `delta` (days relative to today).
        """

        # Prefer scanning all MkDocs pages, not just navigation.
        #
        # Some setups (e.g., auto-generated nav via plugins) can omit pages from
        # navigation while MkDocs still renders them. Timeline should reflect
        # rendered pages with metadata, regardless of nav inclusion.
        doc_pages: list[Any] = []

        pages_var = env.variables.get("pages")
        if pages_var is not None:
            try:
                doc_pages.extend(list(pages_var))
            except TypeError:
                pass

        site = env.variables.get("site")
        if site is not None and hasattr(site, "pages"):
            doc_pages.extend(list(site.pages))

        nav = env.variables.get("navigation") or env.variables.get("nav")
        if nav is not None and hasattr(nav, "pages"):
            doc_pages.extend(list(nav.pages))
        elif nav is not None:
            # Fallback: Walk the nav tree and collect page nodes.
            def walk_nav(items: Iterable[Any]) -> None:
                for item in items:
                    if getattr(item, "is_page", False):
                        doc_pages.append(item)
                    elif getattr(item, "is_section", False):
                        walk_nav(getattr(item, "children", []))

            root_items = getattr(nav, "items", None)
            if root_items is None:
                root_items = nav
            walk_nav(root_items)

        # De-duplicate (site.pages and nav.pages can overlap).
        unique_pages: dict[str, Any] = {}
        for p in doc_pages:
            abs_path = getattr(getattr(p, "file", None), "abs_src_path", None)
            url = getattr(p, "url", None)
            key = str(abs_path or url or id(p))
            if key not in unique_pages:
                unique_pages[key] = p

        doc_pages = list(unique_pages.values())

        current_date = datetime.date.today()
        relevant_items: list[RecentItem] = []

        for p in doc_pages:
            # We only care about pages with a `date` in their metadata.
            meta = _extract_page_meta(p)
            item_date = _coerce_date(meta.get("date"))
            if item_date is None:
                continue

            # Normalize "threads" to a list of strings.
            threads: list[str]
            threads_raw = meta.get("threads", [])

            if threads_raw is None:
                threads = []
            elif isinstance(threads_raw, str):
                threads = [t.strip() for t in threads_raw.split(",") if t.strip()]
            else:
                # If a YAML list is provided, accept it as-is (best effort).
                threads = [str(t).strip() for t in threads_raw if str(t).strip()]

            # Keep items within the last `_RECENT_DAYS` days, and all future items.
            delta = (item_date - current_date).days
            if -_RECENT_DAYS <= delta:
                relevant_items.append(
                    {
                        "title": getattr(p, "title", None) or meta.get("title", "Untitled"),
                        "url": getattr(p, "url", ""),
                        "date": item_date,
                        "type": meta.get("type", "General"),
                        "code": "" if meta.get("code") is None else str(meta.get("code")).strip(),
                        "threads": threads,
                        "due": _coerce_date(meta.get("due")),
                        "delta": delta,
                    }
                )

        # Fallback: scan the docs directory directly.
        #
        # Some navigation configurations omit pages from nav (while MkDocs still
        # renders them). Scanning docs/ ensures we also include those pages.
        existing_urls = {item["url"] for item in relevant_items if item.get("url")}

        docs_dir = _get_docs_dir(env)
        if docs_dir:
            for abs_path in _iter_markdown_files(docs_dir):
                meta = _extract_file_meta(abs_path)
                item_date = _coerce_date(meta.get("date"))
                if item_date is None:
                    continue

                url = _docs_path_to_url(docs_dir, abs_path)
                if url in existing_urls:
                    continue

                threads_raw = meta.get("threads", [])
                if threads_raw is None:
                    threads = []
                elif isinstance(threads_raw, str):
                    threads = [t.strip() for t in threads_raw.split(",") if t.strip()]
                else:
                    threads = [str(t).strip() for t in threads_raw if str(t).strip()]

                delta = (item_date - current_date).days
                if -_RECENT_DAYS <= delta:
                    relevant_items.append(
                        {
                            "title": str(meta.get("title", "Untitled")),
                            "url": url,
                            "date": item_date,
                            "type": str(meta.get("type", "General")),
                            "code": "" if meta.get("code") is None else str(meta.get("code")).strip(),
                            "threads": threads,
                            "due": _coerce_date(meta.get("due")),
                            "delta": delta,
                        }
                    )
                    existing_urls.add(url)

        # Sort reverse-chronologically (newest first).
        relevant_items.sort(key=lambda x: x["date"], reverse=True)

        try:
            limit_int = int(limit)
        except Exception:
            limit_int = 0

        if limit_int and limit_int > 0:
            return relevant_items[:limit_int]

        return relevant_items

    @env.filter
    def format_threads(threads: Iterable[str] | None) -> str:
        """Format a list of thread tags for display.

        Args:
            threads: An iterable of thread/tag strings.

        Returns:
            An HTML string of pill-styled labels.
        """

        if not threads:
            return ""

        pills: list[Markup] = []
        for raw in threads:
            label = str(raw).strip()
            if not label:
                continue
            slug = _slugify_thread(label)
            pills.append(
                Markup('<span class="thread-pill thread-pill--')
                + escape(slug)
                + Markup('">')
                + escape(label)
                + Markup("</span>")
            )

        return str(Markup(" ").join(pills))

    @env.filter
    def format_timeline_date(value: Any) -> str:
        """Format a date for the Timeline subheading.

        Example: 2026-01-09 -> "Friday, January 9th"
        """

        d = _coerce_date(value)
        if d is None:
            return ""
        return _format_long_date_with_ordinal(d)

    @env.filter
    def format_due_date(value: Any) -> str:
        """Format a date for the Due column.

        Example: 2026-01-13 -> "Tue, 1/13"
        """
        d = _coerce_date(value)
        if d is None:
            return ""
        return d.strftime("%a, %-m/%-d")


# ---------------------------------------------------------------------------
# Configuration / conventions
# ---------------------------------------------------------------------------

# Accept a couple of common date formats in page metadata.
_DATE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d")

# How far back (in days) we consider content "recent".
_RECENT_DAYS = 14


_THREAD_SLUG_RE = re.compile(r"[^a-z0-9-]+")


def _ordinal_suffix(day: int) -> str:
    if 11 <= (day % 100) <= 13:
        return "th"
    match day % 10:
        case 1:
            return "st"
        case 2:
            return "nd"
        case 3:
            return "rd"
        case _:
            return "th"


def _format_long_date_with_ordinal(d: datetime.date) -> str:
    return f"{d.strftime('%A, %B')} {d.day}{_ordinal_suffix(d.day)}"


def _slugify_thread(label: str) -> str:
    """Convert a thread label into a CSS-safe slug.

    Example: "API Design" -> "api-design"
    """

    slug = label.strip().lower()
    slug = slug.replace("_", " ")
    slug = re.sub(r"\s+", "-", slug)
    slug = _THREAD_SLUG_RE.sub("", slug)
    return slug.strip("-") or "thread"


def _coerce_date(value: Any) -> datetime.date | None:
    """Coerce a metadata value into a `datetime.date`.

    This macro reads dates from Markdown front matter / metadata where the
    value may be represented as:

    - A `datetime.date`
    - A `datetime.datetime`
    - A string in one of a small set of accepted formats

    Args:
        value: The raw metadata value.

    Returns:
        A `datetime.date` if `value` can be interpreted as a date; otherwise
        `None`.
    """

    if value is None:
        return None

    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value

    if isinstance(value, str):
        for fmt in _DATE_FORMATS:
            try:
                return datetime.datetime.strptime(value, fmt).date()
            except ValueError:
                continue

    return None


def _extract_page_meta(page: Any) -> dict[str, Any]:
    """Extract metadata from a page source file (best effort).

    MkDocs pages often expose `page.meta`, but that can be unavailable or
    incomplete depending on build order and plugin timing. This helper reads the
    page's source Markdown and tries two common metadata styles:

    1) YAML front matter:
       ---
       key: value
       ---

    2) Markdown "meta" header lines at the top of the file:
       key: value
       other: thing

    Args:
        page: A MkDocs page-like object (typically `mkdocs.structure.pages.Page`)
            as exposed via the mkdocs-macros-plugin environment.

    Returns:
        A dict of parsed metadata keys/values. Returns an empty dict if the
        source path is missing or metadata cannot be parsed.
    """

    page_meta = getattr(page, "meta", None)
    if isinstance(page_meta, dict) and page_meta:
        return cast(dict[str, Any], page_meta)

    abs_path = getattr(getattr(page, "file", None), "abs_src_path", None)
    if not abs_path:
        return {}

    return _extract_file_meta(abs_path)


def _extract_file_meta(abs_path: str) -> dict[str, Any]:
    """Extract metadata directly from a Markdown file path (best effort)."""

    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return {}

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # YAML front matter
    if text.startswith("---\n") and "\n---\n" in text:
        fm, _rest = text.split("\n---\n", 1)
        fm = fm[4:]  # strip initial '---\n'

        if yaml is None:
            return {}

        try:
            loaded = yaml.safe_load(fm) or {}
        except Exception:
            return {}

        if isinstance(loaded, dict):
            return cast(dict[str, Any], loaded)
        return {}

    # Markdown meta extension style: key: value until first blank line
    meta: dict[str, Any] = {}
    for line in text.split("\n"):
        if not line.strip():
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta


def _get_docs_dir(env: Any) -> str | None:
    config = env.variables.get("config")
    docs_dir = getattr(config, "docs_dir", None)
    if isinstance(docs_dir, str) and docs_dir:
        return docs_dir
    if isinstance(config, dict):
        val = config.get("docs_dir")
        if isinstance(val, str) and val:
            return val
    return None


def _iter_markdown_files(docs_dir: str) -> list[str]:
    root = Path(docs_dir)
    if not root.exists():
        return []

    paths: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.lower().endswith(".md"):
                paths.append(str(Path(dirpath) / filename))
    return paths


def _docs_path_to_url(docs_dir: str, abs_path: str) -> str:
    """Convert a docs-relative Markdown path to a MkDocs-like URL."""

    root = Path(docs_dir).resolve()
    p = Path(abs_path).resolve()
    try:
        rel = p.relative_to(root).as_posix()
    except ValueError:
        rel = p.name

    if rel.endswith(".md"):
        rel = rel[: -len(".md")]

    # MkDocs maps `index.md` to its containing directory URL.
    if rel == "index":
        return ""
    if rel.endswith("/index"):
        rel = rel[: -len("/index")]

    return f"{rel}/"
