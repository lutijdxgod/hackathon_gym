"""created Prepared Workouts

Revision ID: 434fc3bde50d
Revises: e09d25e015d6
Create Date: 2024-11-01 23:48:45.338498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "434fc3bde50d"
down_revision = "30fcb8a36570"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "prepared_workouts",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_prepared_workouts")),
    )
    op.create_table(
        "favorite_workouts",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("workout_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_favorite_workouts_user_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["workout_id"],
            ["prepared_workouts.id"],
            name=op.f("fk_favorite_workouts_workout_id_prepared_workouts"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_favorite_workouts")),
    )
    op.create_table(
        "prepared_workouts_exercises",
        sa.Column("workout_id", sa.Integer(), nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("sets", sa.Integer(), nullable=False),
        sa.Column("repetitions", sa.Integer(), nullable=False),
        sa.Column("weight", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["exercise_id"],
            ["exercises.id"],
            name=op.f("fk_prepared_workouts_exercises_exercise_id_exercises"),
        ),
        sa.ForeignKeyConstraint(
            ["workout_id"],
            ["prepared_workouts.id"],
            name=op.f("fk_prepared_workouts_exercises_workout_id_prepared_workouts"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_prepared_workouts_exercises")),
    )


def downgrade() -> None:
    op.drop_table("prepared_workouts_exercises")
    op.drop_table("favorite_workouts")
    op.drop_table("prepared_workouts")
