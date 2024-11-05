"""initial version of a db

Revision ID: ef77ff2bb3a3
Revises: 
Create Date: 2024-10-25 01:03:44.123236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ef77ff2bb3a3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "equipment",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("image_url", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_equipment")),
    )
    op.create_table(
        "gyms",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("image_url", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_gyms")),
    )
    op.create_table(
        "muscle_groups",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("image_url", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_muscle_groups")),
    )
    op.create_table(
        "user_verification",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("phone_number", sa.String(length=10), nullable=False),
        sa.Column("verification_code", sa.String(length=4), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_verification")),
        sa.UniqueConstraint("user_id", name=op.f("uq_user_verification_user_id")),
    )
    op.create_table(
        "users",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("surname", sa.String(), nullable=False),
        sa.Column("phone_number", sa.String(length=10), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_table(
        "exercises",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("equipment_id", sa.Integer(), nullable=False),
        sa.Column("muscle_group_id", sa.Integer(), nullable=False),
        sa.Column(
            "difficulty",
            sa.Enum("beginner", "intermediate", "advanced", name="traininglevel"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["equipment_id"],
            ["equipment.id"],
            name=op.f("fk_exercises_equipment_id_equipment"),
        ),
        sa.ForeignKeyConstraint(
            ["muscle_group_id"],
            ["muscle_groups.id"],
            name=op.f("fk_exercises_muscle_group_id_muscle_groups"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_exercises")),
    )
    op.create_table(
        "subscriptions",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("gym_id", sa.Integer(), nullable=False),
        sa.Column("end_time", sa.TIMESTAMP(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(["gym_id"], ["gyms.id"], name=op.f("fk_subscriptions_gym_id_gyms")),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_subscriptions_user_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_subscriptions")),
    )
    op.create_table(
        "user_info",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("sex", sa.Enum("male", "female", name="sex"), nullable=False),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.Column("date_of_birthday", sa.TIMESTAMP(), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("height", sa.Integer(), nullable=False),
        sa.Column(
            "training_level",
            sa.Enum("beginner", "intermediate", "advanced", name="traininglevel"),
            nullable=False,
        ),
        sa.Column(
            "training_frequency",
            sa.Enum("low", "medium", "high", name="trainingfrequency"),
            nullable=False,
        ),
        sa.Column(
            "training_purpose",
            sa.Enum(
                "gaining_weight",
                "gaining_muscle_weight",
                "losing_fat",
                "maintainig",
                name="trainingpurpose",
            ),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_user_info_user_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_info")),
    )
    op.create_table(
        "exercise_media",
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("type", sa.Enum("image", "video", name="mediatype"), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["exercise_id"],
            ["exercises.id"],
            name=op.f("fk_exercise_media_exercise_id_exercises"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_exercise_media")),
    )


def downgrade() -> None:
    op.drop_table("exercise_media")
    op.drop_table("user_info")
    op.drop_table("subscriptions")
    op.drop_table("exercises")
    op.drop_table("users")
    op.drop_table("user_verification")
    op.drop_table("muscle_groups")
    op.drop_table("gyms")
    op.drop_table("equipment")
