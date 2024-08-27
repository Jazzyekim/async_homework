from fastapi import APIRouter

from cve_vault.routes.cve_route import cve_api

api_route = APIRouter(prefix="/api")
api_route.include_router(cve_api)