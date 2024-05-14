"""empty message

Revision ID: b2efd4060ec0
Revises: 
Create Date: 2024-05-07 13:06:39.192601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2efd4060ec0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('component',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_component'))
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_role')),
    sa.UniqueConstraint('name', name=op.f('uq_role_name'))
    )
    op.create_table('type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_type'))
    )
    op.create_table('workshop',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('trace_id', sa.String(), nullable=True),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_workshop')),
    sa.UniqueConstraint('trace_id', name=op.f('uq_workshop_trace_id'))
    )
    op.create_table('drone',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('trace_id', sa.String(), nullable=True),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=True),
    sa.Column('price_drone', sa.Float(), nullable=False),
    sa.Column('weight_drone', sa.Integer(), nullable=False),
    sa.Column('width', sa.Float(), nullable=False),
    sa.Column('length', sa.Float(), nullable=False),
    sa.Column('height', sa.Float(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('instructions', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['type_id'], ['type.id'], name=op.f('fk_drone_type_id_type')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_drone')),
    sa.UniqueConstraint('trace_id', name=op.f('uq_drone_trace_id'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('trace_id', sa.String(), nullable=True),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('surname', sa.String(length=32), nullable=False),
    sa.Column('patronymics', sa.String(length=32), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=32), nullable=False),
    sa.Column('data_bith', sa.Date(), nullable=True),
    sa.Column('passport_series', sa.String(length=4), nullable=True),
    sa.Column('passport_number', sa.String(length=10), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], name=op.f('fk_users_role_id_role')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('trace_id', name=op.f('uq_users_trace_id'))
    )
    op.create_table('drone_to_сomponents',
    sa.Column('id_drone', sa.Integer(), nullable=False),
    sa.Column('id_component', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_component'], ['component.id'], name=op.f('fk_drone_to_сomponents_id_component_component')),
    sa.ForeignKeyConstraint(['id_drone'], ['drone.id'], name=op.f('fk_drone_to_сomponents_id_drone_drone')),
    sa.PrimaryKeyConstraint('id_drone', 'id_component', name=op.f('pk_drone_to_сomponents'))
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('trace_id', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('datatime_order', sa.DateTime(), nullable=False),
    sa.Column('type_order', sa.Enum('in_hall', 'with_myself', name='typeorder'), nullable=True),
    sa.Column('status_order', sa.Enum('waiting_for_payment', 'paid', 'waiting_for_confirmation', 'confirmed', 'prepared', 'ready', 'waiting_for_the_courier', 'delivery', 'completed', name='statusorder'), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_order_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_order')),
    sa.UniqueConstraint('trace_id', name=op.f('uq_order_trace_id'))
    )
    op.create_table('order_to_drone',
    sa.Column('id_order', sa.Integer(), nullable=False),
    sa.Column('id_drone', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_drone'], ['drone.id'], name=op.f('fk_order_to_drone_id_drone_drone')),
    sa.ForeignKeyConstraint(['id_order'], ['order.id'], name=op.f('fk_order_to_drone_id_order_order')),
    sa.PrimaryKeyConstraint('id_order', 'id_drone', name=op.f('pk_order_to_drone'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_to_drone')
    op.drop_table('order')
    op.drop_table('drone_to_сomponents')
    op.drop_table('users')
    op.drop_table('drone')
    op.drop_table('workshop')
    op.drop_table('type')
    op.drop_table('role')
    op.drop_table('component')
    # ### end Alembic commands ###
