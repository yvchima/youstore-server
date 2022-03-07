"""empty message

Revision ID: e82755ff7df4
Revises: 
Create Date: 2022-03-05 09:01:14.712351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e82755ff7df4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('merchant',
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('store_name', sa.String(length=255), nullable=False),
    sa.Column('slug', sa.String(length=255), nullable=False),
    sa.Column('store_location', sa.String(length=255), nullable=True),
    sa.Column('store_photo', sa.String(length=255), nullable=True),
    sa.Column('store_banner', sa.String(length=255), nullable=True),
    sa.Column('fullName', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('phone', sa.String(length=14), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_merchant_email'), 'merchant', ['email'], unique=True)
    op.create_index(op.f('ix_merchant_slug'), 'merchant', ['slug'], unique=True)
    op.create_table('user',
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstName', sa.String(length=255), nullable=False),
    sa.Column('lastName', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('phone', sa.String(length=14), nullable=True),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('photo', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_address'), 'user', ['address'], unique=False)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_firstName'), 'user', ['firstName'], unique=False)
    op.create_index(op.f('ix_user_lastName'), 'user', ['lastName'], unique=False)
    op.create_index(op.f('ix_user_phone'), 'user', ['phone'], unique=False)
    op.create_table('product',
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('slug', sa.String(length=255), nullable=False),
    sa.Column('category', sa.String(length=255), nullable=False),
    sa.Column('sub_category', sa.String(length=255), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('colors', sa.Text(), nullable=True),
    sa.Column('sizes', sa.Text(), nullable=True),
    sa.Column('images', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('inventory', sa.Integer(), nullable=True),
    sa.Column('discount', sa.Float(), nullable=False),
    sa.Column('merchant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_category'), 'product', ['category'], unique=False)
    op.create_index(op.f('ix_product_slug'), 'product', ['slug'], unique=True)
    op.create_index(op.f('ix_product_sub_category'), 'product', ['sub_category'], unique=False)
    op.create_table('wishlist',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'product_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wishlist')
    op.drop_index(op.f('ix_product_sub_category'), table_name='product')
    op.drop_index(op.f('ix_product_slug'), table_name='product')
    op.drop_index(op.f('ix_product_category'), table_name='product')
    op.drop_table('product')
    op.drop_index(op.f('ix_user_phone'), table_name='user')
    op.drop_index(op.f('ix_user_lastName'), table_name='user')
    op.drop_index(op.f('ix_user_firstName'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_address'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_merchant_slug'), table_name='merchant')
    op.drop_index(op.f('ix_merchant_email'), table_name='merchant')
    op.drop_table('merchant')
    # ### end Alembic commands ###