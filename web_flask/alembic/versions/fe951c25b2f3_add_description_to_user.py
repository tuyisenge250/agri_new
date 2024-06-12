"""add description to user

Revision ID: fe951c25b2f3
Revises: 
Create Date: 2024-06-13 00:10:04.630574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'fe951c25b2f3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('news', 'image')
    op.alter_column('resource', 'content',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=60),
               existing_nullable=False)
    op.create_foreign_key(None, 'resource', 'products', ['crops'], ['id'])
    op.drop_column('users', 'description')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('description', mysql.VARCHAR(length=255), nullable=False))
    op.drop_constraint(None, 'resource', type_='foreignkey')
    op.alter_column('resource', 'content',
               existing_type=sa.String(length=60),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=False)
    op.add_column('news', sa.Column('image', mysql.VARCHAR(length=255), nullable=False))
    # ### end Alembic commands ###
