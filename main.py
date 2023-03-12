from fastapi import FastAPI
from app.database import connect_to_mongo, close_mongo_connection
from app.routes.partners import router as partner_router

app = FastAPI()

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(partner_router)
