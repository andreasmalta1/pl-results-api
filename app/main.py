from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.routers import team, match, nation
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
# Prep script for initial data
# Prep script to update every match played
# Prep how to update to new season (new season env var will not work)
# Prep to deploy

## nations
### get_nation
### get_nations
### post_nation
### update nation
### delete nation

## managers
### get_manager
### get_all managers
#### get current // non-current
#### get by nations
#### get by club
### post mnager
### update manager
### delete manager
