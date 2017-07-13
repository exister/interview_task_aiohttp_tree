from tree.handlers import insert, search, subtree


def setup_routes(app):
    app.router.add_post('/insert', insert)
    app.router.add_get('/search', search)
    app.router.add_get('/subtree/{id:\d+}', subtree)
