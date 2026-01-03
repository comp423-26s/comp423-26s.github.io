import datetime

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


def _coerce_date(value):
    if value is None:
        return None
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
            try:
                return datetime.datetime.strptime(value, fmt).date()
            except ValueError:
                pass
    return None


def _extract_page_meta(page):
    """Best-effort metadata extraction from page source.

    We don't rely on `page.meta` because, depending on build order and plugins,
    it may not be populated when the homepage is rendered.
    """
    abs_path = getattr(getattr(page, "file", None), "abs_src_path", None)
    if not abs_path:
        return {}

    try:
        text = open(abs_path, "r", encoding="utf-8").read()
    except OSError:
        return {}

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # YAML front matter
    if text.startswith("---\n") and "\n---\n" in text:
        fm, _rest = text.split("\n---\n", 1)
        fm = fm[4:]  # strip initial '---\n'
        if yaml is not None:
            try:
                loaded = yaml.safe_load(fm) or {}
                if isinstance(loaded, dict):
                    return loaded
            except Exception:
                return {}
        return {}

    # Markdown meta extension style: key: value until first blank line
    meta = {}
    for line in text.split("\n"):
        if not line.strip():
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta

def define_env(env):
    """
    This is the hook for defining variables, macros and filters.
    """

    @env.macro
    def get_recent_and_upcoming(limit=5):
        """
        Returns a list of pages tagged with dates, sorted by date.
        Filters for items from the last 2 weeks or coming up in the future.
        """
        
        # SIMPLER APPROACH: Iterate through the flat list of pages provided by mkdocs
        # effectively available via env.variables['pages'] if you enable certain contexts,
        # but often it is easier to just look at the 'navigation' object.
        
        nav = env.variables.get("navigation") or env.variables.get("nav")

        # Best: MkDocs Navigation exposes a flat list of pages.
        if nav is not None and hasattr(nav, "pages"):
            doc_pages = list(nav.pages)
        else:
            # Fallback: walk the nav tree.
            doc_pages = []

            def walk_nav(items):
                for item in items:
                    if getattr(item, "is_page", False):
                        doc_pages.append(item)
                    elif getattr(item, "is_section", False):
                        walk_nav(getattr(item, "children", []))

            if nav is not None:
                walk_nav(nav)

        current_date = datetime.date.today()
        relevant_items = []

        for p in doc_pages:
            # We only care about pages with a 'date' in frontmatter
            meta = _extract_page_meta(p)
            item_date = _coerce_date(meta.get("date"))
            if item_date is None:
                continue

            threads = meta.get("threads", [])
            if isinstance(threads, str):
                threads = [t.strip() for t in threads.split(",") if t.strip()]
                
                # Logic: Keep if it's within last 14 days OR in the future
            delta = (item_date - current_date).days
            if -14 <= delta:
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

        # Sort by date
        relevant_items.sort(key=lambda x: x["date"])

        try:
            limit_int = int(limit)
        except Exception:
            limit_int = 0

        if limit_int and limit_int > 0:
            return relevant_items[:limit_int]

        return relevant_items

    @env.filter
    def format_threads(threads):
        """Helper to format tags nicely"""
        if not threads: return ""
        return ", ".join(f"`{t}`" for t in threads)
