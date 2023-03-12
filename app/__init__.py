import asyncio

from fastapi import FastAPI

from app.database import partners_collection
from app.routes import partners
from app.seed_data import seed_partners

app = FastAPI()

app.include_router(partners.router, tags=["partners"])


@app.on_event("startup")
async def startup():
    await seed_partners()


if __name__ == "__main__":
    asyncio.run(startup())
