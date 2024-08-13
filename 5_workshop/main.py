import asyncio
import multiprocessing as mp
import os
import time
from concurrent.futures import ProcessPoolExecutor
from contextlib import contextmanager

from functions import _process_file_chunk

# link to download: http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-1gram-20120701-a.gz
FILE_PATH = "./googlebooks-eng-all-1gram-20120701-a"
WORD = "adjR2"


@contextmanager
def timer(msg: str):
    start = time.perf_counter()
    yield
    print(f"{msg}: {time.perf_counter() - start:.2f} seconds")


def get_file_chunks(
        file_name: str,
        max_cpu: int = 8,
) -> tuple[int, list[tuple[str, int, int]]]:
    """Split flie into chunks"""
    cpu_count = min(max_cpu, mp.cpu_count())

    file_size = os.path.getsize(file_name)
    chunk_size = file_size // cpu_count

    start_end = list()
    with open(file_name, mode="r+b") as f:

        def is_new_line(position):
            if position == 0:
                return True
            else:
                f.seek(position - 1)
                return f.read(1) == b"\n"

        def next_line(position):
            f.seek(position)
            f.readline()
            return f.tell()

        chunk_start = 0
        while chunk_start < file_size:
            chunk_end = min(file_size, chunk_start + chunk_size)

            while not is_new_line(chunk_end):
                chunk_end -= 1

            if chunk_start == chunk_end:
                chunk_end = next_line(chunk_end)

            start_end.append(
                (
                    file_name,
                    chunk_start,
                    chunk_end,
                )
            )

            chunk_start = chunk_end

    return (
        cpu_count,
        start_end,
    )


def reduce_words(target: dict, source: dict) -> dict:
    for key, value in source.items():
        if key in target:
            target[key] += value
        else:
            target[key] = value
    return target


async def process_file(
        batches: list,
) -> None:
    loop = asyncio.get_event_loop()
    words = {}
    with ProcessPoolExecutor() as executor:
        with timer("Processing data"):
            results = []
            for batch in batches:
                filename, start, end = batch
                results.append(
                    loop.run_in_executor(executor, _process_file_chunk, filename, start, end)
                )
            done, _ = await asyncio.wait(results)

    with timer("Reducing results"):
        for result in done:
            words = reduce_words(words, result.result())

    print("Total words: ", len(words))
    print("Total count of word : ", words[WORD])


if __name__ == "__main__":
    with timer("Total time"):
        cpu_count, *start_end = get_file_chunks(FILE_PATH)
        asyncio.run(process_file(start_end[0]))
