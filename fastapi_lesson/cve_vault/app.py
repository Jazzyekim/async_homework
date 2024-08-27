from contextlib import asynccontextmanager

from fastapi import FastAPI
from cve_vault.routes.router import api_route

@asynccontextmanager
async def lifespan(_app: FastAPI):
    from cve_vault.deps import get_settings
    from cve_vault.db.db import Base, get_engine

    engine = get_engine(get_settings())

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

app = FastAPI(title = "CVE Vault", lifespan=lifespan)
app.include_router(api_route)