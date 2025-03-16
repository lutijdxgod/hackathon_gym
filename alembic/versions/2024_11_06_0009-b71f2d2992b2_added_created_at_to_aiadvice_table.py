"""added created_at to AIAdvice table

Revision ID: b71f2d2992b2
Revises: a5e54cf49372
Create Date: 2024-11-06 00:09:26.361080

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b71f2d2992b2"
down_revision = "a5e54cf49372"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("ai_advice", sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False))


def downgrade() -> None:
    op.drop_column("ai_advice", "created_at")
