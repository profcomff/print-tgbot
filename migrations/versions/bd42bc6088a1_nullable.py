"""nullable

Revision ID: bd42bc6088a1
Revises: 56584d8792af
Create Date: 2023-02-22 21:18:53.212500

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "bd42bc6088a1"
down_revision = "56584d8792af"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("tg_user", "surname", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("tg_user", "number", existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("tg_user", "number", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("tg_user", "surname", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###
