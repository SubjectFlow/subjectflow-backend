from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient

from app.routers import dbRouter

config = dotenv_values(".env")


app = FastAPI()

app.include_router(dbRouter.router)


@app.on_event("startup")
def startup_db_client():
    print("Connecting to mongo database.")
    app.mongodb_client = MongoClient(config["MONGO_CONNECTION_STRING"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connection completed.")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/favicon.ico")
async def favicon():
    return None


@app.get("/status")
async def status():
    return {"progress": "25%"}
