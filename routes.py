from fastapi import APIRouter, Body, Request, HTTPException
from typing import List, Optional

from models import Movie, MovieUpdate

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
