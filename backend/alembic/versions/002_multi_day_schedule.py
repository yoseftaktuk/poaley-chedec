"""Multi-day schedule support migration."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "002_multi_day_schedule"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("prayer_times", sa.Column("days_of_week", JSONB, server_default="[]"))
    op.execute("UPDATE prayer_times SET days_of_week = jsonb_build_array(day_of_week)")
    op.drop_column("prayer_times", "day_of_week")

    op.add_column("torah_lessons", sa.Column("days_of_week", JSONB, server_default="[]"))
    op.execute("UPDATE torah_lessons SET days_of_week = jsonb_build_array(day_of_week)")
    op.drop_column("torah_lessons", "day_of_week")

    op.add_column("banner_messages", sa.Column("days_of_week", JSONB, server_default="[]"))

    op.add_column("mikveh", sa.Column("opening_schedules", JSONB, server_default="[]"))
    op.execute(
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
    op.drop_column("mikveh", "opening_hours")


def downgrade() -> None:
    op.add_column("mikveh", sa.Column("opening_hours", sa.Text(), server_default=""))
    op.drop_column("mikveh", "opening_schedules")

    op.drop_column("banner_messages", "days_of_week")

    op.add_column("torah_lessons", sa.Column("day_of_week", sa.Integer()))
    op.execute("UPDATE torah_lessons SET day_of_week = (days_of_week->>0)::int")
    op.drop_column("torah_lessons", "days_of_week")

    op.add_column("prayer_times", sa.Column("day_of_week", sa.Integer()))
    op.execute("UPDATE prayer_times SET day_of_week = (days_of_week->>0)::int")
    op.drop_column("prayer_times", "days_of_week")
