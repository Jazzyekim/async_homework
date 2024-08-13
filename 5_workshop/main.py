import asyncio
import time
from concurrent.futures import ProcessPoolExecutor
from contextlib import contextmanager
from itertools import batched
import multiprocessing as mp
from functions import count_words

# link to download: http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-1gram-20120701-a.gz
FILE_PATH = "./googlebooks-eng-all-1gram-20120701-a"
WORD = "языку"


@contextmanager
def timer(msg: str):
    start = time.perf_counter()
    yield
    print(f"{msg}: {time.perf_counter() - start:.2f} seconds")


def reduce_words(target: dict, source: dict) -> dict:
    for key,value in source.items():
        if key in target:
            target[key] += value
        else:
            target[key] = value
    return target


async def main():
    loop = asyncio.get_event_loop()
    words = {}

    with timer("Reading file"):
        with open(FILE_PATH, "r") as file:
            data = file.readlines()

    batch_size = 60_000

    with ProcessPoolExecutor() as executor:
        with timer("Processing data"):
            results = []
            for batch in batched(data, batch_size):
                results.append(
                    loop.run_in_executor(executor, count_words, batch)
                )
            done, _ = await asyncio.wait(results)
        with timer("Reducing results"):
            for result in done:
                words = reduce_words(words, result.result())

    print("Total words: ", len(words))
    print("Total count of word : ", words[WORD])


if __name__ == "__main__":
    # value = mp.Value("i")
    # p = [
    #     mp.Process(target=calculate)
    # ]
    with timer("Total time"):
        asyncio.run(main())
