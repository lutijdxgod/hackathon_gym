"""added training_purpose

Revision ID: e09d25e015d6
Revises: 30fcb8a36570
Create Date: 2024-10-27 00:28:15.155714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e09d25e015d6"
down_revision = "30fcb8a36570"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "user_info",
        sa.Column(
            "training_purpose",
            sa.Enum("gaining_weight", "gaining_muscle_weight", "losing_fat", "maintainig", name="trainingpurpose"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("user_info", "training_purpose")
