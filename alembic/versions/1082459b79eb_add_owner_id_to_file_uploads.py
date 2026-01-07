"""add owner_id to file_uploads

Revision ID: 1082459b79eb
Revises: 4efd9f844139
Create Date: 2026-01-07 21:20:21.254039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1082459b79eb'
down_revision: Union[str, Sequence[str], None] = '4efd9f844139'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('file_uploads', sa.Column('owner_id', sa.Integer(
    ), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True))
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_column('file_uploads', 'owner_id')
    # ### end Alembic commands ###
