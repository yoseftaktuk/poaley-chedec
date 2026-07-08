import re

import bleach

ALLOWED_TAGS = ["p", "br", "strong", "em", "ul", "ol", "li", "a", "h2", "h3"]
ALLOWED_ATTRIBUTES = {"a": ["href", "title", "rel"]}


def sanitize_html(value: str) -> str:
    return bleach.clean(value, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)


def sanitize_text(value: str) -> str:
    without_blocks = re.sub(
        r"<(script|style)\b[^>]*>.*?</\1>",
        "",
        value,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return bleach.clean(without_blocks, tags=[], attributes={}, strip=True).strip()
