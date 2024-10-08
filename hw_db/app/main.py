import contextlib
import logging
import os
import json
import time
from datetime import datetime

import aiofiles
import asyncpg
from pathlib import Path
import sys

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker
from models import Base, ProblemType
from cve_repository import (make_cve, make_problem_type, get_all_cve, get_cve_by_id,
                            get_cve_records_by_date_published, get_cve_records_by_date_updated)

from config import DB_URI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DB_ECHO = os.environ.get("DB_ECHO", "false").lower() == "true"


@contextlib.contextmanager
def perf_time(title: str):
    start = time.perf_counter()
    yield
    print(f"{title} took {time.perf_counter() - start} seconds")


def get_engine() -> AsyncEngine:
    return create_async_engine(
        DB_URI,
        echo=DB_ECHO,
    )


def make_session_class(engine: AsyncEngine) -> type[AsyncSession]:
    return async_sessionmaker(
        engine,
        expire_on_commit=False,
    )


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def process_json_file(session_klass, file_path, cve_batch, problem_type_batch):
    async with session_klass() as session:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
            data = json.loads(content)

            state = data['cveMetadata']['state']
            if state == "PUBLISHED":
                cve_id = data['cveMetadata']['cveId']
                title = data['containers']['adp'][0]['title'] if 'adp' in data['containers'] else ""

                description = data['containers']['cna']['descriptions'][0]['value']

                published_ = data['cveMetadata']['datePublished'] if 'datePublished' in data['cveMetadata'] else \
                    data['cveMetadata']['dateUpdated']

                date_published = datetime.fromisoformat(published_).replace(tzinfo=None)
                date_updated = datetime.fromisoformat(data['cveMetadata']['dateUpdated']).replace(tzinfo=None)
                cve = make_cve(cve_id, title, description, date_published, date_updated)

                cve_batch.append(cve)
                if 'problemTypes' in data['containers']['cna']:
                    for problem_type in data['containers']['cna']['problemTypes']:
                        for description in problem_type['descriptions']:
                            problem_type_entry = make_problem_type(description["description"], cve)
                            problem_type_batch.append(problem_type_entry)



async def scan_directory(session_klass, base_path, batch_size=100):
    cve_batch = []
    problem_type_batch = []

    for dirpath, dirnames, filenames in os.walk(base_path):
        tasks = []
        for filename in filenames:
            if filename.endswith('.json') and filename.startswith("CVE"):
                file_path = os.path.join(dirpath, filename)
                tasks.append(process_json_file(session_klass, file_path, cve_batch, problem_type_batch))

        if tasks:
            await asyncio.gather(*tasks)

        if len(cve_batch) >= batch_size:
            async with session_klass() as session:
                session.add_all(cve_batch)
                session.add_all(problem_type_batch)
                await session.commit()
            cve_batch.clear()
            problem_type_batch.clear()

    if cve_batch or problem_type_batch:
        async with session_klass() as session:
            session.add_all(cve_batch)
            session.add_all(problem_type_batch)
            await session.commit()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py /path/to/cves")
        sys.exit(1)

    base_path = sys.argv[1]
    base_path = Path(base_path)
    if not base_path.exists() or not base_path.is_dir():
        print(f"The provided path '{base_path}' is not a valid directory.")
        sys.exit(1)

    engine = get_engine()
    session_klass = make_session_class(engine)

    await create_tables(engine)

    await scan_directory(session_klass, base_path)

    async with session_klass() as session:
        logger.info("Fetching CVE")
        # for cve in await get_all_cve(session):
        #     print(cve)
        print(await get_cve_by_id(session, "CVE-2004-0008"))
        print(await get_cve_records_by_date_published(session, datetime.fromisoformat("2004-09-01T04:00:00")))
        print(await get_cve_records_by_date_updated(session, datetime.fromisoformat("2024-08-08T00:01:23.639")))

    await drop_tables(engine)


if __name__ == '__main__':
    import asyncio

    with perf_time("Main"):
        asyncio.run(main())
