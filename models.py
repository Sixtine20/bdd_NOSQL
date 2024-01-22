from typing import Optional, List, Union, Dict
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId


class Movie(BaseModel):
    _id: ObjectId
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    runtime: Optional[int] = None
    cast: Optional[List[str]] = None
    poster: Optional[str] = None
    title: Optional[str] = None
    fullplot: Optional[str] = None
    languages: Optional[List[str]] = None
    released: Optional[Union[datetime, dict]] = None
    directors: Optional[List[str]] = None
    rated: Optional[str] = None
    awards: Optional[dict] = None
    lastupdated: Optional[str] = None
    year: Optional[int] = None
    imdb: Optional[dict] = None
    countries: Optional[List[str]] = None
    type: Optional[str] = None
    tomatoes: Optional[dict] = None
    num_mflix_comments: Optional[int] = None

    class Config:
        json_schema_extra = {
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
    released: Optional[Union[datetime, dict]] = None
    directors: Optional[List[str]] = None
    rated: Optional[str] = None
    awards: Optional[dict] = None
    lastupdated: Optional[str] = None
    year: Optional[int] = None
    imdb: Optional[dict] = None
    countries: Optional[List[str]] = None
    type: Optional[str] = None
    tomatoes: Optional[dict] = None
    num_mflix_comments: Optional[int] = None

    class Config:
        json_schema_extra = {
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


class CommonMoviesResponse(BaseModel):
    common_movies_count: int

    class Config:
        json_schema_extra = {
            "example": {
                "common_movies_count": 0
            }
        }