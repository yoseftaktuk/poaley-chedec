import bleach

ALLOWED_TAGS = ["p", "br", "strong", "em", "ul", "ol", "li", "a", "h2", "h3"]
ALLOWED_ATTRIBUTES = {"a": ["href", "title", "rel"]}


def sanitize_html(value: str) -> str:
    return bleach.clean(value, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)


def sanitize_text(value: str) -> str:
    return bleach.clean(value, tags=[], strip=True).strip()
