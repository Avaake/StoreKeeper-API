"""create products table

Revision ID: dc314cc4715f
Revises: f336a43c8449
Create Date: 2024-12-03 17:12:24.282735

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dc314cc4715f"
down_revision = "f336a43c8449"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.VARCHAR(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            name=op.f("fk_products_category_id_categories"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_products")),
        sa.UniqueConstraint("name", name=op.f("uq_products_name")),
    )


def downgrade():
    op.drop_table("products")
