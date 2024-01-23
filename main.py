from fastapi import FastAPI
from dotenv import dotenv_values, load_dotenv
from pymongo import MongoClient
from neo4j import GraphDatabase, basic_auth
from routes import router as movie_router
import os

load_dotenv()

config = dotenv_values(".env")

NEO4J_URI=os.getenv('NEO4J_URI')
NEO4J_USERNAME=os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD=os.getenv('NEO4J_PASSWORD')

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGODB_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

    app.neo4j_driver = GraphDatabase.driver(
        NEO4J_URI, 
        auth=basic_auth(NEO4J_USERNAME, NEO4J_PASSWORD)
    )
    
    print("Connected to the Neo4J database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    app.neo4j_driver.close()

app.include_router(movie_router, tags=["movies"], prefix="/movie")
