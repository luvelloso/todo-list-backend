"""create initial schema

Revision ID: 0001
Revises:
Create Date: 2026-06-15
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    table_names = inspector.get_table_names()

    if "users" not in table_names:
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), primary_key=True, index=True),
            sa.Column("email", sa.String(), nullable=True),
            sa.Column("full_name", sa.String(), nullable=False),
            sa.Column("hashed_password", sa.String(), nullable=True),
        )
        op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
        op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    if "todos" not in table_names:
        op.create_table(
            "todos",
            sa.Column("id", sa.Integer(), primary_key=True, index=True),
            sa.Column("title", sa.String(), nullable=True),
            sa.Column("description", sa.String(), nullable=True),
            sa.Column(
                "category",
                sa.Enum("DESIGN", "PERSONAL", "HOUSE", "WORK", "HEALTH", name="todocategory"),
                nullable=False,
            ),
            sa.Column(
                "status",
                sa.Enum("PENDING", "COMPLETED", name="todostatus"),
                nullable=False,
            ),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.Column("scheduled_date", sa.Date(), nullable=False),
            sa.Column("owner_id", sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        )
        op.create_index(op.f("ix_todos_id"), "todos", ["id"], unique=False)
        op.create_index(op.f("ix_todos_title"), "todos", ["title"], unique=False)
    else:
        todo_columns = {column["name"] for column in inspector.get_columns("todos")}
        if "description" not in todo_columns:
            op.add_column("todos", sa.Column("description", sa.String(), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    table_names = inspector.get_table_names()

    if "todos" in table_names:
        todo_columns = {column["name"] for column in inspector.get_columns("todos")}
        if "description" in todo_columns:
            op.drop_column("todos", "description")
