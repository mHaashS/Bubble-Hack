"""Add stripe_customer_id to users table

Revision ID: add_stripe_customer_id
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_stripe_customer_id'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Ajouter la colonne stripe_customer_id à la table users
    op.add_column('users', sa.Column('stripe_customer_id', sa.String(), nullable=True))
    op.create_index(op.f('ix_users_stripe_customer_id'), 'users', ['stripe_customer_id'], unique=True)


def downgrade():
    # Supprimer l'index et la colonne
    op.drop_index(op.f('ix_users_stripe_customer_id'), table_name='users')
    op.drop_column('users', 'stripe_customer_id')
