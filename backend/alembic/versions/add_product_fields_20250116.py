"""Add product fields code supplier_price price commission

Revision ID: add_product_fields_20250116
Revises: ace5a0c417b3
Create Date: 2025-01-16 19:25:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_product_fields_20250116'
down_revision = 'ace5a0c417b3'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to products table
    op.add_column('products', sa.Column('code', sa.String(), nullable=True))
    op.add_column('products', sa.Column('supplier_price', sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column('products', sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column('products', sa.Column('commission', sa.Numeric(precision=10, scale=2), nullable=True))
    
    # Create index on code column
    op.create_index(op.f('ix_products_code'), 'products', ['code'], unique=False)


def downgrade():
    # Remove index
    op.drop_index(op.f('ix_products_code'), table_name='products')
    
    # Remove columns
    op.drop_column('products', 'commission')
    op.drop_column('products', 'price')
    op.drop_column('products', 'supplier_price')
    op.drop_column('products', 'code')