import asyncio
from asyncio import StreamReader, StreamWriter


async def get_data(reader: StreamReader):
    while True:
        data = await reader.read(1024)
        if not data:
            break
        print(f"Received: {data.decode()}")


async def start_client():
    reader, writer = await asyncio.open_connection(host="localhost", port=8888)
    try:
        await get_data(reader)
    except asyncio.CancelledError:
        pass
    finally:
        writer.close()
        await writer.wait_closed()


if __name__ == "__main__":
    asyncio.run(start_client())
