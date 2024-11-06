"""created AIAdvice table

Revision ID: 35ea30f6cc0c
Revises: b4ce0f08b57f
Create Date: 2024-11-05 22:51:52.008838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "35ea30f6cc0c"
down_revision = "b4ce0f08b57f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ai_advice",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("type", sa.Enum("training_plan", "progress", name="advicetype"), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_ai_advice_user_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_ai_advice")),
    )


def downgrade() -> None:
    op.drop_table("ai_advice")
