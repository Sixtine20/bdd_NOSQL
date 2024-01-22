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

print("NEO4J_URI:", NEO4J_URI)

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGODB_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(movie_router, tags=["movies"], prefix="/movie")



driver = GraphDatabase.driver(
    NEO4J_URI, 
    auth=basic_auth(NEO4J_USERNAME, NEO4J_PASSWORD)
)

cypher_query = '''
MATCH (movie:Movie {title:$favorite})<-[:ACTED_IN]-(actor)-[:ACTED_IN]->(rec:Movie)
 RETURN distinct rec.title as title LIMIT 20
'''

with driver.session(database="neo4j") as session:
  results = session.read_transaction(
    lambda tx: tx.run(cypher_query,
                      favorite="The Matrix").data())
  for record in results:
    print(record['title'])

driver.close()
