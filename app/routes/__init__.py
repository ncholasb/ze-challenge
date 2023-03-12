from fastapi import APIRouter
from app.routes import partners

router = APIRouter()

router.include_router(partners.router)
