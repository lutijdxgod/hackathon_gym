"""added todays_muscle_group_id_field

Revision ID: a5e54cf49372
Revises: 35ea30f6cc0c
Create Date: 2024-11-05 23:11:23.264019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a5e54cf49372"
down_revision = "35ea30f6cc0c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("user_info", sa.Column("todays_muscle_group_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        op.f("fk_user_info_todays_muscle_group_id_muscle_groups"),
        "user_info",
        "muscle_groups",
        ["todays_muscle_group_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_user_info_todays_muscle_group_id_muscle_groups"), "user_info", type_="foreignkey")
    op.drop_column("user_info", "todays_muscle_group_id")
