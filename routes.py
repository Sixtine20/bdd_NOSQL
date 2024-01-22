from fastapi import APIRouter, Body, Request, HTTPException
from typing import List, Optional

from models import Movie, MovieUpdate, CommonMoviesResponse

router = APIRouter()

@router.get("/", response_description="List all movies", response_model=List[Movie])
def list_movies(request: Request):
    # Récupérer la liste de films depuis MongoDB
    movies = list(request.app.database["movies"].find(limit=100))
    return movies

@router.get("/common-movies", response_description="List common movies between MongoDB and Neo4j", response_model=CommonMoviesResponse)
def get_common_movies(request: Request):
    # Récupérer la liste de films depuis MongoDB
    movies_mongodb = list(request.app.database["movies"].find())

    # Exécuter la requête Cypher pour récupérer les films en commun et en compter le nombre
    cypher_query = '''
    MATCH (movie:Movie)
    WHERE movie.title IN $titles
    RETURN count(distinct movie) as count
    '''

    with request.app.neo4j_driver.session(database="neo4j") as session:
        results = session.read_transaction(
            lambda tx: tx.run(cypher_query, titles=[movie["title"] for movie in movies_mongodb]).data()
        )

    # Récupérer le nombre total
    common_movies_count = sum(record['count'] for record in results)

    return CommonMoviesResponse(common_movies_count=common_movies_count)


@router.get("/{param}", response_description="Get a single movie by title or actor name", response_model=Movie)
def find_movie(param: str, request: Request):
    # Créer une requête de recherche MongoDB avec une condition OR
    search_query = {
        "$or": [
            {"title": {"$regex": f".*{param}.*", "$options": "i"}},
            {"cast": {"$in": [param]}}
        ]
    }

    # Rechercher le film dans la base de données MongoDB
    if (movie := request.app.database["movies"].find_one(search_query)) is not None:
        # Convertir l'ID MongoDB en une chaîne pour la sortie JSON
        movie["_id"] = str(movie["_id"])
        # Retourner le film trouvé
        return movie

    # Si aucun film n'est trouvé, lever une exception HTTP 404
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with title or actor '{param}' not found")


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
