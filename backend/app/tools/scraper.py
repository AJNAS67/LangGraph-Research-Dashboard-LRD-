import re
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode


def normalize_url(url: str) -> str:
    """Normalizes a URL by lowercasing scheme/host, removing trailing slashes,

    and stripping marketing/tracking query parameters (e.g., utm_*, fbclid).
    """
    if not url:
        return ""

    parsed = urlparse(url.strip())
    # Normalize scheme and netloc to lowercase
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    # Normalize path (strip trailing slash if not root)
    path = parsed.path
    if len(path) > 1 and path.endswith("/"):
        path = path[:-1]

    # Filter out tracking query parameters
    tracking_params = {
        "utm_source", "utm_medium", "utm_campaign", "utm_term",
        "utm_content", "fbclid", "gclid", "ref", "source"
    }
    filtered_queries = [
        (k, v) for k, v in parse_qsl(parsed.query)
        if k.lower() not in tracking_params
    ]
    query = urlencode(filtered_queries)

    # Omit fragments (#heading) for deduplication
    return urlunparse((scheme, netloc, path, parsed.params, query, ""))


def sanitize_text(text: str, max_chars: int = 1500) -> str:
    """Sanitizes raw text extracts from web results by removing excessive

    whitespace, HTML remnants, and truncating to max characters.
    """
    if not text:
        return ""

    # Remove any stray HTML tags
    cleaned = re.sub(r"<[^>]+>", " ", text)
    # Collapse multiple whitespace/newlines
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    if len(cleaned) > max_chars:
        return cleaned[:max_chars] + "..."
    return cleaned
