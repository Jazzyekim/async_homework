from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route


async def homepage(request):
    return HTMLResponse("<h1>Hello Starlette World</h1>")

routes = [
    Route('/', homepage)
]

app = Starlette(debug=True, routes=routes)

