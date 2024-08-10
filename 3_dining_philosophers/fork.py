import asyncio


class Fork:
    def __init__(self, fork_number: int):
        self.lock = asyncio.Lock()
        self.fork_number = fork_number
