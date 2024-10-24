"""added dificulty column to Exercise

Revision ID: 8621c65d0cb9
Revises: 730841b1172d
Create Date: 2024-10-24 18:22:07.876053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8621c65d0cb9"
down_revision = "730841b1172d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "exercises",
        sa.Column("difficulty", sa.Enum("beginner", "intermediate", "advanced", name="traininglevel"), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("exercises", "difficulty")
