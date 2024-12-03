"""create categories table

Revision ID: f336a43c8449
Revises: cc0f86644eed
Create Date: 2024-12-03 17:10:50.747229

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f336a43c8449"
down_revision = "cc0f86644eed"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.VARCHAR(length=30), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_categories")),
        sa.UniqueConstraint("name", name=op.f("uq_categories_name")),
    )


def downgrade():
    op.drop_table("categories")
