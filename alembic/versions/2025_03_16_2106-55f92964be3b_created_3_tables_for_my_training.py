"""Created 3 tables for My Training

Revision ID: 55f92964be3b
Revises: b71f2d2992b2
Create Date: 2025-03-16 21:06:31.868683

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "55f92964be3b"
down_revision = "b71f2d2992b2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "gym_equipments",
        sa.Column("gym_id", sa.Integer(), nullable=False),
        sa.Column("equipment_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["equipment_id"], ["equipment.id"], name=op.f("fk_gym_equipments_equipment_id_equipment")
        ),
        sa.ForeignKeyConstraint(["gym_id"], ["gyms.id"], name=op.f("fk_gym_equipments_gym_id_gyms")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_gym_equipments")),
    )
    op.create_table(
        "my_training",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("training_frequency", sa.Enum("low", "medium", "high", name="trainingfrequency"), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_my_training_user_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_my_training")),
    )
    op.create_table(
        "my_training_exercises",
        sa.Column("training_id", sa.Integer(), nullable=False),
        sa.Column("sets", sa.Integer(), nullable=False),
        sa.Column("repetitions", sa.Integer(), nullable=False),
        sa.Column("exercise_name", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["training_id"],
            ["my_training.id"],
            name=op.f("fk_my_training_exercises_training_id_my_training"),
            ondelete="cascade",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_my_training_exercises")),
    )
    op.add_column(
        "user_info",
        sa.Column(
            "training_frequency",
            sa.Enum("low", "medium", "high", name="trainingfrequency"),
            nullable=False,
            server_default="low",
        ),
    )


def downgrade() -> None:
    op.drop_column("user_info", "training_frequency")
    op.drop_table("my_training_exercises")
    op.drop_table("my_training")
    op.drop_table("gym_equipments")
