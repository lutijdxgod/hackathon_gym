"""added image_url to Exercise

Revision ID: 30fcb8a36570
Revises: 213806c6185f
Create Date: 2024-10-26 02:05:08.048979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "30fcb8a36570"
down_revision = "213806c6185f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("exercises", sa.Column("image_url", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("exercises", "image_url")
