"""empty message

Revision ID: e7c3679510d2
Revises: 
Create Date: 2022-11-02 16:43:03.878164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7c3679510d2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('description', sa.String(length=2000), nullable=False),
    sa.Column('category', sa.String(length=200), nullable=False),
    sa.Column('image_url', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('inventories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=2000), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment_methods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('credit_number', sa.String(length=16), nullable=False),
    sa.Column('expiry_date', sa.String(length=5), nullable=False),
    sa.Column('security_number', sa.String(length=4), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('star_rating', sa.Integer(), nullable=False),
    sa.Column('review_details', sa.String(length=1000), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_items')
    op.drop_table('reviews')
    op.drop_table('payment_methods')
    op.drop_table('orders')
    op.drop_table('inventories')
    op.drop_table('users')
    op.drop_table('items')
    # ### end Alembic commands ###
