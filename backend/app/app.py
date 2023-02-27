import csv
from fastapi import FastAPI, HTTPException, APIRouter, Query
from typing import Optional, Any



app = FastAPI()

api_router = APIRouter()

movie_path = '../../MovieSummaries/movies.csv'

# Read data from CSV file and store in list of dictionaries
with open(movie_path, newline="") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    movies = [row for row in reader]

print(movies[0])

# define a function to filter data based on search terms
def filter_data(movies,
    movie_name: Optional[str] = None,
    character_name: Optional[str] = None,
    actor_name: Optional[str] = None,
    actor_gender: Optional[str] = None,
    release_year: Optional[str] = None
):

    filtered_data = movies

    if movie_name: 
        filtered_data = [item for item in filtered_data if item["Movie_name"].lower() == movie_name.lower()]
    if character_name: 
        filtered_data = [item for item in filtered_data if item["Character_name"].lower() == character_name.lower()]
    if actor_name: 
        filtered_data = [item for item in filtered_data if item["Actor_name"].lower() == actor_name.lower()]
    if actor_gender: 
        filtered_data = [item for item in filtered_data if item["Actor_gender"].lower() == actor_gender.lower()]
    if release_year: 
        filtered_data = [item for item in filtered_data if item["Movie_release_date_cm"].lower() == release_year]
   
    return filtered_data
   

# home route - currently a placeholder
@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Welcome to the Movie Machine!"}


# download route - currently a placeholder
@api_router.get("/download", status_code=200)
async def get_movies():
    return {'movies': movies}


# Define endpoint to get movies
@app.get("/movies")
async def get_movies(
    movie_name: str = None,
    character_name: str = None,
    actor_name: str = None,
    actor_gender: str = None,
    release_year: Optional[str] = None
):
    filtered_data = filter_data(movies, movie_name,character_name, actor_name, actor_gender, release_year)

    if not filtered_data:
        raise HTTPException(status_code=404, detail="Movies not found")

    return filtered_data



app.include_router(api_router)

if __name__ == "__main__":
    # use for debugging only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8032, log_level="debug")
