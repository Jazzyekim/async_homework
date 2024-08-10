import asyncio
from fork import Fork
from philosopher import Philosopher


async def main():
    forks = [Fork(i) for i in range(5)]
    philosopher_names = ["Socrates", "Plato", "Aristotle", "Descartes", "Kant"]
    philosophers = [
        Philosopher(philosopher_names[i], forks[i], forks[(i + 1) % 5])
        for i in range(5)
    ]

    await asyncio.gather(*(ph.dine() for ph in philosophers))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Philosophers stopped dining.")
