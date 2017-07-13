import json
import base64

import functools
from sqlalchemy import and_, ARRAY, INTEGER, cast
from sqlalchemy.dialects.postgresql import array
from aiohttp import web

from .models import tree_table, get_node, insert_node


AUTH = {
    'admin': 'admin'
}

async def is_authenticated(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return False

    try:
        auth_type, auth_info = auth_header.split(None, 1)
        auth_type = auth_type.lower()
    except ValueError:
        return False

    if auth_type != 'basic':
        return False

    try:
        username, password = base64.b64decode(auth_info).split(b':', 1)
    except Exception:
        return False

    return AUTH.get(username.decode()) == password.decode()


def require_auth(f):
    @functools.wraps(f)
    async def wrapped(request):
        if not await is_authenticated(request):
            raise web.HTTPUnauthorized()
        return await f(request)
    return wrapped


@require_auth
async def insert(request):
    """
    ---
    tags:
    - tree
    summary: Insert node
    produces:
    - application/json
    parameters:
    - in: body
      name: body
      description: Insert node
      required: true
      schema:
        type: object
        properties:
          parent_id:
            type: integer
            format: int64
          text:
            type: string
    responses:
      "201":
        description: Node inserted
      "404":
        description: Parent node not found
    security:
      - api_key: []
    """
    data = await request.json()
    parent_id = data.get('parent_id')
    text = data.get('text', '')

    path = []
    if parent_id:
        parent = await get_node(node_id=parent_id, db=request.app['db'])
        if not parent:
            return web.HTTPBadRequest(
                text=json.dumps({"parent_id": "Not found"}),
                content_type='application/json'
            )
        path = parent['path'][:]
        path.append(parent['id'])

    new_row = await insert_node(text=text, path=path, db=request.app['db'])

    return web.HTTPCreated(
        text=json.dumps(
            {
                "id": new_row.id,
                "text": text,
                "path": path
            }
        ),
        content_type='application/json'
    )


@require_auth
async def search(request):
    """
    ---
    tags:
    - tree
    summary: Search nodes
    produces:
    - application/json
    parameters:
    - in: query
      name: q
      required: false
      type: string
    responses:
      "200":
        description:
    """

    data = []
    query = request.query.get('q')
    if query:
        async with request.app['db'].acquire() as conn:
            data = [
                dict(row.items())
                async for row in conn.execute(tree_table.select().where(tree_table.c.text.match(query)))
            ]

    return web.HTTPOk(
        text=json.dumps(data),
        content_type='application/json'
    )

@require_auth
async def subtree(request):
    """
    ---
    tags:
    - tree
    summary: Get subtree
    produces:
    - application/json
    parameters:
    - in: path
      name: id
      required: true
      type: string
    responses:
      "200":
        description:
    """
    item_id = int(request.match_info.get('id'))

    item = await get_node(node_id=item_id, db=request.app['db'])
    if not item:
        return web.HTTPNotFound()

    async with request.app['db'].acquire() as conn:
        data = [
            dict(row.items())
            async for row in conn.execute(
                tree_table.select().where(
                    and_(
                        tree_table.c.id != item_id,
                        array([tree_table.c.id]).overlap(cast(item.path, ARRAY(INTEGER())))
                    )
                ).order_by(tree_table.c.path)
            )
        ]

    return web.HTTPOk(
        text=json.dumps(data),
        content_type='application/json'
    )