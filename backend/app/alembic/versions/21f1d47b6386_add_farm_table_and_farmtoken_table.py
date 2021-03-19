"""Add farm table and farmtoken table

Revision ID: 21f1d47b6386
Revises: d4867f3a4c0a
Create Date: 2020-01-29 00:53:26.627087

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "21f1d47b6386"
down_revision = "d4867f3a4c0a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "farm",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "time_created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("time_updated", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_accessed", sa.DateTime(timezone=True), nullable=True),
        sa.Column("farm_name", sa.String(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("tags", sa.String(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.Column("info", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("is_authorized", sa.Boolean(), nullable=True),
        sa.Column("auth_error", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_farm_farm_name"), "farm", ["farm_name"], unique=False)
    op.create_index(op.f("ix_farm_id"), "farm", ["id"], unique=False)
    op.create_index(op.f("ix_farm_url"), "farm", ["url"], unique=True)
    op.create_table(
        "farmtoken",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("access_token", sa.String(), nullable=True),
        sa.Column("expires_in", sa.String(), nullable=True),
        sa.Column("refresh_token", sa.String(), nullable=True),
        sa.Column("expires_at", sa.String(), nullable=True),
        sa.Column("farm_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["farm_id"], ["farm.id"],),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("farm_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("farmtoken")
    op.drop_index(op.f("ix_farm_url"), table_name="farm")
    op.drop_index(op.f("ix_farm_id"), table_name="farm")
    op.drop_index(op.f("ix_farm_farm_name"), table_name="farm")
    op.drop_table("farm")
    # ### end Alembic commands ###
