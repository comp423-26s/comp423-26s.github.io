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
from typing import Any, Iterable, TypedDict, cast

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
    threads: list[str]
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
    def get_recent_and_upcoming(limit: int | str = 5) -> list[RecentItem]:
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

        # We prefer iterating over MkDocs' navigation structure because it
        # reflects exactly what will be rendered.
        nav = env.variables.get("navigation") or env.variables.get("nav")

        # Best case: Navigation exposes a flat list of pages.
        doc_pages: list[Any]
        if nav is not None and hasattr(nav, "pages"):
            doc_pages = list(nav.pages)
        else:
            # Fallback: Walk the nav tree and collect page nodes.
            doc_pages = []

            def walk_nav(items: Iterable[Any]) -> None:
                for item in items:
                    if getattr(item, "is_page", False):
                        doc_pages.append(item)
                    elif getattr(item, "is_section", False):
                        walk_nav(getattr(item, "children", []))

            if nav is not None:
                walk_nav(nav)

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
                        "threads": threads,
                        "delta": delta,
                    }
                )

        # Sort chronologically.
        relevant_items.sort(key=lambda x: x["date"])

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
            A comma-separated string with each tag wrapped in backticks.
        """

        if not threads:
            return ""
        return ", ".join(f"`{t}`" for t in threads)


# ---------------------------------------------------------------------------
# Configuration / conventions
# ---------------------------------------------------------------------------

# Accept a couple of common date formats in page metadata.
_DATE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d")

# How far back (in days) we consider content "recent".
_RECENT_DAYS = 14


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

    abs_path = getattr(getattr(page, "file", None), "abs_src_path", None)
    if not abs_path:
        return {}

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
            # Best effort typing: YAML keys/values may not be strings.
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
