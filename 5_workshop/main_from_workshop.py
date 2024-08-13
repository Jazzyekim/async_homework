import asyncio
import time
from concurrent.futures import ProcessPoolExecutor
from contextlib import contextmanager
from itertools import batched
import multiprocessing as mp
from functions import count_words

# link to download: http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-1gram-20120701-a.gz
FILE_PATH = "./googlebooks-eng-all-1gram-20120701-a"
WORD = "adjR2"


@contextmanager
def timer(msg: str):
    start = time.perf_counter()
    yield
    print(f"{msg}: {time.perf_counter() - start:.2f} seconds")


def reduce_words(target: dict, source: dict) -> dict:
    for key, value in source.items():
        if key in target:
            target[key] += value
        else:
            target[key] = value
    return target


async def monitoring(counter, counter_lock, total):
    interval_seconds = 5

    while True:
        # with counter_lock:
        print(f"Progress: {counter.value}/{total}")
        if counter.value == total:
            break
        await asyncio.sleep(interval_seconds)


async def main():
    loop = asyncio.get_event_loop()
    words = {}

    with timer("Reading file"):
        with open(FILE_PATH, "r") as file:
            data = file.readlines()

    batch_size = 60_000
    with mp.Manager() as manager:
        counter = manager.Value("i", 0)
        counter_lock = manager.Lock()

        monitoring_task = asyncio.shield(asyncio.create_task(monitoring(counter, counter_lock, len(data))))

        with ProcessPoolExecutor() as executor:
            with timer("Processing data"):
                results = []
                for batch in batched(data, batch_size):
                    results.append(
                        loop.run_in_executor(executor, count_words, batch, counter, counter_lock)
                    )
                done, _ = await asyncio.wait(results)
            with timer("Reducing results"):
                for result in done:
                    words = reduce_words(words, result.result())

        monitoring_task.cancel()

    print("Total words: ", len(words))
    print("Total count of word : ", words[WORD])


if __name__ == "__main__":
    with timer("Total time"):
        asyncio.run(main())
