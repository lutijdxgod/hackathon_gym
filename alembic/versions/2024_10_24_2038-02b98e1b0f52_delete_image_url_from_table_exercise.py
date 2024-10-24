"""delete image_url from table Exercise

Revision ID: 02b98e1b0f52
Revises: 8621c65d0cb9
Create Date: 2024-10-24 20:38:11.239841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "02b98e1b0f52"
down_revision = "8621c65d0cb9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("exercises", "image_url")


def downgrade() -> None:
    op.add_column("exercises", sa.Column("image_url", sa.VARCHAR(), autoincrement=False, nullable=False))
