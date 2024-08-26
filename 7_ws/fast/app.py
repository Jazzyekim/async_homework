from fastapi import FastAPI

from starlette.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return """
    <html>
        <head>
            <title>Hello World</title>
        </head>
        <body>
            <h1>Hello, World!</h1>
        </body>
    </html>
    """
