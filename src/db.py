from aiopg.sa import create_engine
from sqlalchemy.schema import CreateTable, DropTable

from tree.models import tree_table


async def init_db(app):
    settings = app['conf']['db']
    app['db'] = await create_engine(**settings, echo=True)


async def close_db(app):
    app['db'].close()
    await app['db'].wait_closed()
    app['db'] = None


async def create_table(app):
    async with app['db'].acquire() as conn:
        # await conn.execute(DropTable(tree_table))
        await conn.execute(CreateTable(tree_table))
