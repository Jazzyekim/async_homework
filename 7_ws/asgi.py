async def app(scope, receive, send):
    if scope["type"] != "http":
        return

    await receive()

    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"text/html"],
            ],
        }
    )

    await send(
        {
            "type": "http.response.body",
            "body": b"<h1>Hello Async World :)</h1>",
        }
    )