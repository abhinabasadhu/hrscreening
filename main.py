from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from route.routes_candidate import router as candidate_router
from route.routes_job import router as job_router

config = dotenv_values(".env")
ATLAS_URI = 'mongodb+srv://abhinaba_sadhu:wHBklGAN1Sj1fCl7@hrscreening.rceywem.mongodb.net/'
DB_NAME = 'hrscreening'

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(ATLAS_URI)
    app.database = app.mongodb_client[DB_NAME]


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(candidate_router, tags=["candidates"], prefix="/candidate")
app.include_router(job_router, tags=["jobs"], prefix="/job")
