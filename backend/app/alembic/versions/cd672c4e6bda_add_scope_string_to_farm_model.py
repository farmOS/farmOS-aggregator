"""Add scope string to Farm model

Revision ID: cd672c4e6bda
Revises: 21f1d47b6386
Create Date: 2020-02-04 03:00:30.105475

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "cd672c4e6bda"
down_revision = "21f1d47b6386"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("farm", sa.Column("scope", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("farm", "scope")
    # ### end Alembic commands ###
