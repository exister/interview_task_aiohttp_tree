import sqlalchemy as sa

from sqlalchemy.dialects import postgresql


metadata = sa.MetaData()

tree_table = sa.Table(
    "tree", metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('text', sa.String(255)),
    sa.Column('path', postgresql.ARRAY(sa.Integer)),
)

async def get_node(node_id: int,  db):
    async with db.acquire() as conn:
        result = await conn.execute(
            tree_table.select().where(tree_table.c.id == node_id)
        )
        return await result.fetchone()


async def insert_node(text: str, path: list, db):
    async with db.acquire() as conn:
        result = await conn.execute(
            tree_table.insert().values(text=text, path=path).returning(tree_table.c.id)
        )
        return await result.fetchone()
