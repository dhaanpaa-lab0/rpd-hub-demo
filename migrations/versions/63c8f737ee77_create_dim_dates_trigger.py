"""create_dim_dates_trigger

Revision ID: 63c8f737ee77
Revises: f7150fffc717
Create Date: 2025-11-30 11:23:20.578079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63c8f737ee77'
down_revision: Union[str, Sequence[str], None] = 'f7150fffc717'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create trigger function and trigger for dim_dates table."""
    # Create the trigger function
    op.execute("""
        CREATE OR REPLACE FUNCTION populate_dim_dates_fields()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Extract date components from the date field
            NEW.day := EXTRACT(DAY FROM NEW.date);
            NEW.week := EXTRACT(WEEK FROM NEW.date);
            NEW.month := EXTRACT(MONTH FROM NEW.date);
            NEW.quarter := EXTRACT(QUARTER FROM NEW.date);
            NEW.year := EXTRACT(YEAR FROM NEW.date);
            NEW.day_of_week := EXTRACT(DOW FROM NEW.date);

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Create the trigger
    op.execute("""
        DROP TRIGGER IF EXISTS trg_populate_dim_dates ON dim_dates;

        CREATE TRIGGER trg_populate_dim_dates
            BEFORE INSERT OR UPDATE ON dim_dates
            FOR EACH ROW
            EXECUTE FUNCTION populate_dim_dates_fields();
    """)


def downgrade() -> None:
    """Remove trigger and trigger function for dim_dates table."""
    # Drop the trigger first
    op.execute("DROP TRIGGER IF EXISTS trg_populate_dim_dates ON dim_dates;")

    # Drop the trigger function
    op.execute("DROP FUNCTION IF EXISTS populate_dim_dates_fields();")
