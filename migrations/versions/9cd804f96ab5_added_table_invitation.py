"""added table Invitation

Revision ID: 9cd804f96ab5
Revises: 8a5397d0fa64
Create Date: 2024-05-08 09:34:44.530100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cd804f96ab5'
down_revision: Union[str, None] = '8a5397d0fa64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Invitation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('is_accepted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['Company.id'], ),
    sa.ForeignKeyConstraint(['recipient_id'], ['User.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Invitation')
    # ### end Alembic commands ###
