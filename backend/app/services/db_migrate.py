"""Run schema migrations for multi-day schedule support."""

import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

logger = logging.getLogger(__name__)


async def run_schema_migrations(conn: AsyncConnection) -> None:
    await _migrate_prayer_times(conn)
    await _migrate_prayer_times_zmanim(conn)
    await _migrate_torah_lessons(conn)
    await _migrate_banner_messages(conn)
    await _migrate_mikveh(conn)
    await _widen_time_columns(conn)
    await _add_image_public_id_columns(conn)


async def _column_exists(conn: AsyncConnection, table: str, column: str) -> bool:
    result = await conn.execute(
        text(
            """
            SELECT 1 FROM information_schema.columns
            WHERE table_name = :table AND column_name = :column
            """
        ),
        {"table": table, "column": column},
    )
    return result.first() is not None


async def _migrate_prayer_times(conn: AsyncConnection) -> None:
    if await _column_exists(conn, "prayer_times", "days_of_week"):
        return
    if await _column_exists(conn, "prayer_times", "day_of_week"):
        await conn.execute(text("ALTER TABLE prayer_times ADD COLUMN days_of_week JSONB DEFAULT '[]'"))
        await conn.execute(
            text("UPDATE prayer_times SET days_of_week = jsonb_build_array(day_of_week)")
        )
        await conn.execute(text("ALTER TABLE prayer_times DROP COLUMN day_of_week"))
    else:
        await conn.execute(
            text("ALTER TABLE prayer_times ADD COLUMN IF NOT EXISTS days_of_week JSONB DEFAULT '[]'")
        )
    logger.info("Migrated prayer_times to days_of_week")


async def _migrate_prayer_times_zmanim(conn: AsyncConnection) -> None:
    if not await _column_exists(conn, "prayer_times", "time_mode"):
        await conn.execute(
            text("ALTER TABLE prayer_times ADD COLUMN time_mode VARCHAR(20) DEFAULT 'fixed'")
        )
        await conn.execute(text("UPDATE prayer_times SET time_mode = 'fixed' WHERE time_mode IS NULL"))
        logger.info("Added prayer_times.time_mode")

    if not await _column_exists(conn, "prayer_times", "zman_ref"):
        await conn.execute(text("ALTER TABLE prayer_times ADD COLUMN zman_ref VARCHAR(50)"))
        logger.info("Added prayer_times.zman_ref")

    if not await _column_exists(conn, "prayer_times", "offset_minutes"):
        await conn.execute(
            text("ALTER TABLE prayer_times ADD COLUMN offset_minutes INTEGER DEFAULT 0")
        )
        await conn.execute(text("UPDATE prayer_times SET offset_minutes = 0 WHERE offset_minutes IS NULL"))
        logger.info("Added prayer_times.offset_minutes")

    await conn.execute(text("ALTER TABLE prayer_times ALTER COLUMN prayer_time DROP NOT NULL"))


async def _migrate_torah_lessons(conn: AsyncConnection) -> None:
    if await _column_exists(conn, "torah_lessons", "days_of_week"):
        return
    if await _column_exists(conn, "torah_lessons", "day_of_week"):
        await conn.execute(text("ALTER TABLE torah_lessons ADD COLUMN days_of_week JSONB DEFAULT '[]'"))
        await conn.execute(
            text("UPDATE torah_lessons SET days_of_week = jsonb_build_array(day_of_week)")
        )
        await conn.execute(text("ALTER TABLE torah_lessons DROP COLUMN day_of_week"))
    else:
        await conn.execute(
            text("ALTER TABLE torah_lessons ADD COLUMN IF NOT EXISTS days_of_week JSONB DEFAULT '[]'")
        )
    logger.info("Migrated torah_lessons to days_of_week")


async def _migrate_banner_messages(conn: AsyncConnection) -> None:
    if not await _column_exists(conn, "banner_messages", "days_of_week"):
        await conn.execute(
            text("ALTER TABLE banner_messages ADD COLUMN days_of_week JSONB DEFAULT '[]'")
        )
        logger.info("Added days_of_week to banner_messages")


async def _migrate_mikveh(conn: AsyncConnection) -> None:
    if await _column_exists(conn, "mikveh", "opening_schedules"):
        return
    await conn.execute(
        text("ALTER TABLE mikveh ADD COLUMN opening_schedules JSONB DEFAULT '[]'")
    )
    if await _column_exists(conn, "mikveh", "opening_hours"):
        await conn.execute(
            text(
                """
                UPDATE mikveh SET opening_schedules = jsonb_build_array(
                    jsonb_build_object(
                        'days_of_week', jsonb_build_array(0,1,2,3,4,5,6),
                        'hours', opening_hours
                    )
                )
                WHERE opening_hours IS NOT NULL AND opening_hours != ''
                """
            )
        )
        await conn.execute(text("ALTER TABLE mikveh DROP COLUMN opening_hours"))
    logger.info("Migrated mikveh to opening_schedules")


async def _column_max_length(conn: AsyncConnection, table: str, column: str) -> int | None:
    result = await conn.execute(
        text(
            """
            SELECT character_maximum_length
            FROM information_schema.columns
            WHERE table_name = :table AND column_name = :column
            """
        ),
        {"table": table, "column": column},
    )
    row = result.first()
    return row[0] if row else None


async def _widen_time_columns(conn: AsyncConnection) -> None:
    for table, column in (
        ("prayer_times", "prayer_time"),
        ("torah_lessons", "lesson_time"),
        ("events", "event_time"),
    ):
        max_len = await _column_max_length(conn, table, column)
        if max_len is not None and max_len < 50:
            await conn.execute(
                text(f"ALTER TABLE {table} ALTER COLUMN {column} TYPE VARCHAR(50)")
            )
            logger.info("Widened %s.%s to VARCHAR(50)", table, column)


async def _add_image_public_id_columns(conn: AsyncConnection) -> None:
    columns = (
        ("events", "image_public_id"),
        ("mikveh", "image_public_id"),
        ("gallery_albums", "cover_public_id"),
    )
    for table, column in columns:
        if not await _column_exists(conn, table, column):
            await conn.execute(
                text(f"ALTER TABLE {table} ADD COLUMN {column} VARCHAR(300)")
            )
            logger.info("Added %s.%s", table, column)
