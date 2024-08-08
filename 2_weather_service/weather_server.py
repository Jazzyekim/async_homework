import asyncio
import random
from asyncio import StreamWriter, StreamReader


async def send_weather_data(writer:StreamWriter):
    try:
        while True:
            temperature = random.uniform(-30, 40)
            humidity = random.uniform(0, 100)
            wind_speed = random.uniform(0, 20)

            weather_data = f'Temperature: {temperature:.2f}C, Humidity: {humidity:.2f}%, Wind Speed: {wind_speed:.2f}m/s'
            writer.write(weather_data.encode())
            await writer.drain()
            await asyncio.sleep(1)
    except (ConnectionResetError, BrokenPipeError):
        pass


async def handle_client(reader: StreamReader, writer: StreamWriter):
    address = writer.get_extra_info('peername')
    print(f"Client is connected: {address}")

    try:
        await send_weather_data(writer)
    except asyncio.CancelledError:
        pass
    finally:
        try:
            print(f"Client is disconnected")
            writer.close()
            await writer.wait_closed()
        except BrokenPipeError as e:
            pass


async def server_start():
    server = await asyncio.start_server(handle_client, host="localhost", port=8888)
    print("Server started at", "localhost", 8888)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(server_start())
