from aiohttp import web
from aiohttp_swagger import setup_swagger

from db import init_db, close_db, create_table
from routes import setup_routes

app = web.Application()
app['conf'] = {
    'db': {
        'user': 'app_devhub',
        'password': 'app_devhub',
        'database': 'app_devhub',
        'host': 'db',
    }
}

app.on_startup.append(init_db)
app.on_shutdown.append(close_db)

# app.on_startup.append(create_table)

setup_routes(app)
setup_swagger(app)

web.run_app(app, port=8000)
