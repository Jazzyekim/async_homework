import asyncio
from fork import Fork
import random


class Philosopher:
    def __init__(self, name: str, left_fork: Fork, right_fork: Fork):
        self.name = name
        self.left_fork = left_fork
        self.right_fork = right_fork

    async def __take_forks(self):
        print(f"{self.name} is trying to pick up left fork ({self.left_fork.fork_number})")
        async with self.left_fork.lock:
            print(f"{self.name} took left fork ({self.left_fork.fork_number})")

            print(f"{self.name} is trying to pick up right fork ({self.right_fork.fork_number})")
            async with self.right_fork.lock:
                print(f"{self.name} took right fork ({self.right_fork.fork_number})")
                eating_time = random.uniform(1, 5)
                print(f"{self.name} is eating for {eating_time}...")
                await asyncio.sleep(eating_time)

            print(f"{self.name} put down right fork ({self.right_fork.fork_number})")

        print(f"{self.name} put down left fork ({self.left_fork.fork_number})")

    async def dine(self):
        while True:
            thinking_time = random.uniform(1, 5)
            print(f"{self.name} is thinking for {thinking_time} seconds...")
            await asyncio.sleep(thinking_time)

            await self.__take_forks()



