"""create Practice, PracticeExercises

Revision ID: 62cde8cb373e
Revises: e09d25e015d6
Create Date: 2024-10-31 01:00:57.137856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62cde8cb373e'
down_revision = 'e09d25e015d6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('practice',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_practice'))
    )
    op.create_table('practice_exercises',
    sa.Column('practice_id', sa.Integer(), nullable=False),
    sa.Column('exercise_id', sa.Integer(), nullable=False),
    sa.Column('sets', sa.Integer(), nullable=False),
    sa.Column('repetitions', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], name=op.f('fk_practice_exercises_exercise_id_exercises')),
    sa.ForeignKeyConstraint(['practice_id'], ['practice.id'], name=op.f('fk_practice_exercises_practice_id_practice')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_practice_exercises'))
    )


def downgrade() -> None:
    op.drop_table('practice_exercises')
    op.drop_table('practice')
