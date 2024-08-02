import argparse
import asyncio
import os
import sys

import aiohttp
from aiohttp import ClientTimeout


async def fetch(session, url, timeout, idx):
    try:
        async with session.get(url, timeout=timeout) as response:
            content = await response.read()
            with open(f'output_{idx}.html', 'wb') as f:
                f.write(content)
            print(f"Content from {url} saved to output_{idx}.html")
    except asyncio.TimeoutError:
        print(f"TimeoutError: The request to {url} has timed out.")


async def main(urls, timeout_value):
    timeout = ClientTimeout(total=timeout_value)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [fetch(session, url, timeout, idx) for idx, url in enumerate(urls)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Async data fetcher')
    parser.add_argument('--file', "-f", type=str, default="./url.data", help='File containing URLs')
    parser.add_argument('--timeout', "-t", type=int, default=10, help='Timeout for requests in seconds')
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"The file {args.file} does not exist.")
        sys.exit(1)

    with open(args.file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    asyncio.run(main(urls, args.timeout))
