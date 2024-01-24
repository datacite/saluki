"""Add doi property to datafile

Revision ID: e1e943473fa5
Revises: 67994ef648ef
Create Date: 2024-01-24 21:42:35.781291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1e943473fa5'
down_revision: Union[str, None] = '67994ef648ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('datafiles', sa.Column('doi', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('datafiles', 'doi')
    # ### end Alembic commands ###
