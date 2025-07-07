"""Add latitude and longitude to emergency_contacts

Revision ID: e56e0c06cc38
Revises: 0f15972f3d8b
Create Date: 2025-07-07 16:23:07.480875

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e56e0c06cc38'
down_revision: Union[str, None] = '0f15972f3d8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('emergency_contacts', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('emergency_contacts', sa.Column('longitude', sa.Float(), nullable=True))

def downgrade():
    op.drop_column('emergency_contacts', 'latitude')
    op.drop_column('emergency_contacts', 'longitude')
