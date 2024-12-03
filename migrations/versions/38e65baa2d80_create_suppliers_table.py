"""create suppliers table

Revision ID: 38e65baa2d80
Revises: e1b0248a3c3e
Create Date: 2024-12-03 17:16:42.114854

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "38e65baa2d80"
down_revision = "e1b0248a3c3e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "suppliers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.VARCHAR(length=255), nullable=False),
        sa.Column("email", sa.VARCHAR(length=50), nullable=True),
        sa.Column("phone_number", sa.VARCHAR(length=20), nullable=True),
        sa.Column("address", sa.VARCHAR(length=255), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_suppliers")),
        sa.UniqueConstraint("name", name=op.f("uq_suppliers_name")),
    )


def downgrade():
    op.drop_table("suppliers")
