import uuid
from typing import Optional, List, Union, Dict
from datetime import datetime
from pydantic import BaseModel, Field, validator
from bson import ObjectId

class Award(BaseModel):
    wins: Optional[int] = None
    nominations: Optional[int] = None
    text: Optional[str] = None

class Imdb(BaseModel):
    rating: Optional[float] = None
    votes: Optional[int] = None
    id : Optional[int] = None

class ViewerAndCritic(BaseModel):
    rating: Optional[float] = None
    numReviews: Optional[int] = None
    meter : Optional[int] = None

class Tomatoes(BaseModel):
    viewer: Optional[ViewerAndCritic] = None
    fresh: Optional[int] = None
    rotten: Optional[int] = None
    critic: Optional[ViewerAndCritic] = None
    lastUpdated: Optional[datetime] = None

class Movie(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    runtime: Optional[int] = None
    cast: Optional[List[str]] = None
    poster: Optional[str] = None
    title: Optional[str] = None
    fullplot: Optional[str] = None
    languages: Optional[List[str]] = None
    released: Optional[datetime] = None
    directors: Optional[List[str]] = None
    rated: Optional[str] = None
    awards: Optional[Award] = None
    lastupdated: Optional[str] = None
    year: Optional[Union[int, str]] = None
    imdb: Optional[Imdb] = None
    countries: Optional[List[str]] = None
    type: Optional[str] = None
    tomatoes: Optional[Tomatoes] = None
    num_mflix_comments: Optional[int] = None

    @validator('id', pre=True)
    def objectId_str(cls, x):
        if isinstance(x, ObjectId):
            return str(x)
        return x
    
    class Config:
        schema_extra = {
            "example": {
                "_id": {"$oid": "573a1390f29313caabcd6223"},
                "plot": "Gwen's family is rich, but her parents ignore her and most of the servants push her around, so she is lonely and unhappy. Her father is concerned only with making money, and her mother ...",
                "genres": ["Comedy", "Drama", "Family"],
                "runtime": 65,
                "cast": ["Mary Pickford", "Madlaine Traverse", "Charles Wellesley", "Gladys Fairbanks"],
                "title": "The Poor Little Rich Girl",
                "fullplot": "Gwen's family is rich, but her parents ignore her and most of the servants push her around, so she is lonely and unhappy. Her father is concerned only with making money, and her mother cares only about her social position. But one day a servant's irresponsibility creates a crisis that causes everyone to rethink what is important to them.",
                "languages": ["English"],
                "released": {"$date": {"$numberLong": "-1667088000000"}},
                "directors": ["Maurice Tourneur"],
                "writers": ["Eleanor Gates (play)", "Frances Marion (scenario)"],
                "awards": {"wins": 1, "nominations": 0, "text": "1 win."},
                "lastupdated": "2015-07-27 00:11:31.387000000",
                "year": 1917,
                "imdb": {"rating": 6.9, "votes": 884, "id": 8443},
                "countries": ["USA"],
                "type": "movie",
                "tomatoes": {"viewer": {"rating": 3.9, "numReviews": 137, "meter": 77}, "production": "Artcraft",
                             "lastUpdated": {"$date": "2015-08-21T18:00:25Z"}},
                "num_mflix_comments": 0
            }
        }


class MovieUpdate(BaseModel):
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    runtime: Optional[int] = None
    cast: Optional[List[str]] = None
    poster: Optional[str] = None
    title: Optional[str] = None
    fullplot: Optional[str] = None
    languages: Optional[List[str]] = None
    released: Optional[datetime] = None
    directors: Optional[List[str]] = None
    rated: Optional[str] = None
    awards: Optional[Award] = None
    lastupdated: Optional[str] = None
    year: Optional[Union[int, str]] = None
    imdb: Optional[Imdb] = None
    countries: Optional[List[str]] = None
    type: Optional[str] = None
    tomatoes: Optional[Tomatoes] = None
    num_mflix_comments: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "plot": "Gwen's family is rich, but her parents ignore her and most of the servants push her around, so she is lonely and unhappy. Her father is concerned only with making money, and her mother ...",
                "genres": ["Comedy", "Drama", "Family"],
                "runtime": 65,
                "cast": ["Mary Pickford", "Madlaine Traverse", "Charles Wellesley", "Gladys Fairbanks"],
                "title": "The Poor Little Rich Girl",
                "fullplot": "Gwen's family is rich, but her parents ignore her and most of the servants push her around, so she is lonely and unhappy. Her father is concerned only with making money, and her mother cares only about her social position. But one day a servant's irresponsibility creates a crisis that causes everyone to rethink what is important to them.",
                "languages": ["English"],
                "released": {"$date": {"$numberLong": "-1667088000000"}},
                "directors": ["Maurice Tourneur"],
                "writers": ["Eleanor Gates (play)", "Frances Marion (scenario)"],
                "awards": {"wins": 1, "nominations": 0, "text": "1 win."},
                "lastupdated": "2015-07-27 00:11:31.387000000",
                "year": 1917,
                "imdb": {"rating": 6.9, "votes": 884, "id": 8443},
                "countries": ["USA"],
                "type": "movie",
                "tomatoes": {"viewer": {"rating": 3.9, "numReviews": 137, "meter": 77}, "production": "Artcraft",
                             "lastUpdated": {"$date": "2015-08-21T18:00:25Z"}},
                "num_mflix_comments": 0
            }
        }

class RatedMovie(BaseModel):
    tagline: str
    title: str
    released: int

class UserMovies(BaseModel):
    name: str

class User(BaseModel):
    user: UserMovies
    numberOfMovies: int
    ratedMovies: List[RatedMovie]

class UserRatedMovie(BaseModel):
    user: dict

class CommonMoviesResponse(BaseModel):
    common_movies_count: int

    class Config:
        schema_extra = {
            "example": {
                "common_movies_count": 0
            }
        }
