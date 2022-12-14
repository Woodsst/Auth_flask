"""Added account table

Revision ID: 419da2b6e21f
Revises:
Create Date: 2022-10-26 17:59:27.166478

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "419da2b6e21f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("role_id"),
        sa.UniqueConstraint("role"),
    )
    op.create_table(
        "socials",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("login", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("role", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["role"], ["roles.role_id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("login"),
        sa.UniqueConstraint("password"),
    )
    op.create_table(
        "user_social",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("social_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["social_id"], ["socials.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", "user_id", "social_id"),
        sa.UniqueConstraint("url"),
    )
    op.execute(
        "INSERT INTO roles (role, description) "
        "VALUES ('Admin', 'full access')"
    )
    op.execute(
        "INSERT INTO roles (role, description) "
        "VALUES ('User', 'default access')"
    )


def downgrade() -> None:
    op.drop_table("user_social")
    op.drop_table("user_device")
    op.drop_table("users")
    op.drop_table("socials")
    op.drop_table("roles")
    op.drop_table("devices")
