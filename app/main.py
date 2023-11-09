from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.routers import team, match, nation, manager
from app.database import Base, engine


Base.metadata.create_all(bind=engine)


tags_metadata = [
    {
        "name": "Teams",
        "description": "Team information",
    },
]

description = """
"""


app = FastAPI(
    title="PL Results Table",
    description=description,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    version="1.0.0",
    contact={
        "name": "Andreas Calleja",
        "email": "andreascalleja@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(team.router)
app.include_router(match.router)
app.include_router(nation.router)
app.include_router(manager.router)

add_pagination(app)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API KEY
## For now, API Key equals env var
## Create user model, with stored API keys
### https://www.vidavolta.io/fastapi-api-keys/
# Ask seperate API from website
# Deploy website using AWS
# Caching
# Welcome page
# Prep script for initial data
# Prep script to update every match played
# Prep how to update to new season (new season env var will not work)
# Prep to deploy
