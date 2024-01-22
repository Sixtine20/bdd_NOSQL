from fastapi import APIRouter, Body, Request, HTTPException
from typing import List, Optional
from neo4j import basic_auth

from models import Movie, MovieUpdate, User, UserRatedMovie, CommonMoviesResponse


router = APIRouter()

@router.get("/", response_description="List all movies", response_model=List[Movie])
def list_movies(request: Request):
    movies = list(request.app.database["movies"].find(limit=100))
    return movies


@router.get("/{param}", response_description="Get a single movie by title or actor name", response_model=Movie)
def find_movie(param: str, request: Request):
    search_query = {
        "$or": [
            {"title": {"$regex": f".*{param}.*", "$options": "i"}},
            {"cast": {"$in": [param]}}
        ]
    }

    if (movie := request.app.database["movies"].find_one(search_query)) is not None:
        movie["_id"] = str(movie["_id"])
        return movie

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with title or actor '{param}' not found")


@router.get("/common-movies", response_description="List common movies between MongoDB and Neo4j", response_model=CommonMoviesResponse)
def get_common_movies(request: Request):
    movies_mongodb = list(request.app.database["movies"].find())

    cypher_query = '''
    MATCH (movie:Movie)
    WHERE movie.title IN $titles
    RETURN count(distinct movie) as count
    '''

    with request.app.neo4j_driver.session(database="neo4j") as session:
        results = session.read_transaction(
            lambda tx: tx.run(cypher_query, titles=[movie["title"] for movie in movies_mongodb]).data()
        )

    common_movies_count = sum(record['count'] for record in results)

    return CommonMoviesResponse(common_movies_count=common_movies_count)


@router.get("/neo4j/rated/{title}", response_description="list users who rated a movie", response_model=List[UserRatedMovie])
def neo4j_get_users_rated(title: str, request: Request):

    cypher_query = '''
    MATCH (movie:Movie {title: $title})<-[r]-(user:Person)
    WHERE r.rating IS NOT NULL
    RETURN user
    '''

    with request.app.neo4j_driver.session(database="neo4j") as session:
        results = session.read_transaction(
            lambda tx: tx.run(cypher_query, title=title).data())
        
        return results
    
    
@router.get("/neo4j/user/{name}", response_description="a user with the number of movies he has rated and the list of rated movies", response_model=List[User])
def neo4j_get_user(name: str, request: Request):

    cypher_query = '''
    MATCH (user:Person {name: $name})
    OPTIONAL MATCH (user)-[r]->(movie:Movie)
    WHERE r.rating IS NOT NULL
    RETURN user, COALESCE(COUNT(r.rating), 0) AS numberOfMovies, COLLECT(movie) AS ratedMovies
    '''

    with request.app.neo4j_driver.session(database="neo4j") as session:
        results = session.read_transaction(
            lambda tx: tx.run(cypher_query, name=name).data())
        
        return results


@router.put("/{title}", response_description="Update a movie", response_model=Movie)
def update_movie(title: str, request: Request, movie_update: MovieUpdate = Body(...)):
    movie = {k: v for k, v in movie_update.dict().items() if v is not None}
    if len(movie) >= 1:
        update_result = request.app.database["movies"].update_one(
            {"title": title}, {"$set": movie}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with title '{title}' not found")

    if (
        existing_movie := request.app.database["movies"].find_one({"title": title})
    ) is not None:
        return existing_movie

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with title '{title}' not found")

