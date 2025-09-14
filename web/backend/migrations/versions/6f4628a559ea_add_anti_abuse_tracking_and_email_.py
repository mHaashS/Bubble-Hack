"""Add anti-abuse tracking and email verification

Revision ID: 6f4628a559ea
Revises: dfa36ccfa50d
Create Date: 2025-09-13 23:19:17.983231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f4628a559ea'
down_revision: Union[str, Sequence[str], None] = 'dfa36ccfa50d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Créer la table email_verifications
    op.create_table('email_verifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_used', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_email_verifications_id'), 'email_verifications', ['id'], unique=False)
    op.create_index(op.f('ix_email_verifications_token'), 'email_verifications', ['token'], unique=True)

    # Créer la table abuse_tracking
    op.create_table('abuse_tracking',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ip_address', sa.String(), nullable=False),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('device_fingerprint', sa.String(), nullable=True),
        sa.Column('email_domain', sa.String(), nullable=True),
        sa.Column('account_count', sa.Integer(), nullable=True),
        sa.Column('last_activity', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_abuse_tracking_id'), 'abuse_tracking', ['id'], unique=False)
    op.create_index(op.f('ix_abuse_tracking_ip_address'), 'abuse_tracking', ['ip_address'], unique=False)
    op.create_index(op.f('ix_abuse_tracking_device_fingerprint'), 'abuse_tracking', ['device_fingerprint'], unique=False)
    op.create_index(op.f('ix_abuse_tracking_email_domain'), 'abuse_tracking', ['email_domain'], unique=False)
    op.create_index('ix_abuse_tracking_ip_device', 'abuse_tracking', ['ip_address', 'device_fingerprint'], unique=False)
    op.create_index('ix_abuse_tracking_ip_domain', 'abuse_tracking', ['ip_address', 'email_domain'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Supprimer les tables dans l'ordre inverse
    op.drop_index('ix_abuse_tracking_ip_domain', table_name='abuse_tracking')
    op.drop_index('ix_abuse_tracking_ip_device', table_name='abuse_tracking')
    op.drop_index(op.f('ix_abuse_tracking_email_domain'), table_name='abuse_tracking')
    op.drop_index(op.f('ix_abuse_tracking_device_fingerprint'), table_name='abuse_tracking')
    op.drop_index(op.f('ix_abuse_tracking_ip_address'), table_name='abuse_tracking')
    op.drop_index(op.f('ix_abuse_tracking_id'), table_name='abuse_tracking')
    op.drop_table('abuse_tracking')
    
    op.drop_index(op.f('ix_email_verifications_token'), table_name='email_verifications')
    op.drop_index(op.f('ix_email_verifications_id'), table_name='email_verifications')
    op.drop_table('email_verifications')
