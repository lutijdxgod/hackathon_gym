"""added training_level column to a PreparedWorkout table

Revision ID: b4ce0f08b57f
Revises: 434fc3bde50d
Create Date: 2024-11-03 16:09:50.442627

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b4ce0f08b57f"
down_revision = "434fc3bde50d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "prepared_workouts",
        sa.Column(
            "training_level", sa.Enum("beginner", "intermediate", "advanced", name="traininglevel"), nullable=False
        ),
    )


def downgrade() -> None:
    op.drop_column("prepared_workouts", "training_level")
