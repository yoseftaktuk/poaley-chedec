from typing import Any

from app.services.image_cleanup import safe_delete_image


def prepare_image_field_updates(
    item: Any,
    updates: dict[str, Any],
    *,
    url_field: str,
    public_id_field: str,
) -> tuple[dict[str, Any], str | None, str | None, Any]:
    if updates.get(url_field) and updates.get(public_id_field) is None:
        updates.pop(public_id_field, None)

    old_public_id = getattr(item, public_id_field)
    new_public_id = updates.get(public_id_field, old_public_id)
    new_url = updates.get(url_field, getattr(item, url_field))

    if url_field in updates and not new_url:
        updates[public_id_field] = None

    return updates, old_public_id, new_public_id, new_url


def cleanup_replaced_image(
    old_public_id: str | None,
    new_public_id: str | None,
    updates: dict[str, Any],
    *,
    url_field: str,
    new_url: Any,
) -> None:
    if old_public_id and old_public_id != new_public_id:
        safe_delete_image(old_public_id)
    if url_field in updates and not new_url and old_public_id:
        safe_delete_image(old_public_id)
