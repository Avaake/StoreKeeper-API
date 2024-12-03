"""create supplies table

Revision ID: 29d91596ebed
Revises: 38e65baa2d80
Create Date: 2024-12-03 17:17:35.814038

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "29d91596ebed"
down_revision = "38e65baa2d80"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "supplies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_name", sa.VARCHAR(length=255), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("price", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("supplier_id", sa.Integer(), nullable=True),
        sa.Column("delivery_date", sa.DateTime(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("pending", "delivery", "cancelled", name="supply_status"),
            server_default="pending",
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["supplier_id"],
            ["suppliers.id"],
            name=op.f("fk_supplies_supplier_id_suppliers"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_supplies")),
    )


def downgrade():
    op.drop_table("supplies")
