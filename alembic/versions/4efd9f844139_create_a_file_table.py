"""create a file table

Revision ID: 4efd9f844139
Revises: ec2418163a8f
Create Date: 2026-01-07 13:42:47.643884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4efd9f844139'
down_revision: Union[str, Sequence[str], None] = 'ec2418163a8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('file_uploads',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('filename', sa.String(), nullable=False),
                    sa.Column('data', sa.LargeBinary(), nullable=False),
                    sa.Column('uploaded_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('file_uploads')
    pass
