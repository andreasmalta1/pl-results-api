from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from pathlib import Path

from app import Base, engine
from app.routers import team, match, nation, manager, stints, home, contact, admin


Base.metadata.create_all(bind=engine)


tags_metadata = [
    {
        "name": "Teams",
        "description": "Information about all the teams to have particapted in the Premier League",
    },
    {
        "name": "Matches",
        "description": "All the matches from the 1992/1993 to today. Contains the score, date and season",
    },
    {
        "name": "Nations",
        "description": "All the nations that PL managers have come from",
    },
    {
        "name": "Managers",
        "description": "All managers to have taken charge of a PL side (excludes caretaker managers)",
    },
    {
        "name": "ManagerialStints",
        "description": "All managerial stints in the PL era, including current managers",
    },
]

description = """A Premier League Results API.\n
Query all the teams to have played in the PL, all the matches that have been played and all the managers in the PL from 1992 to this day.\n
Updated daily with the latest information.\n
Message me for feedback, help and any errors found in the data.\n
Register for an API key to use.\n
FREE FOR USE. Please use responsibly!!!
"""


app = FastAPI(
    title="PL Results API",
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

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)
app.include_router(team.router)
app.include_router(match.router)
app.include_router(nation.router)
app.include_router(manager.router)
app.include_router(stints.router)
app.include_router(home.router)
app.include_router(contact.router)
app.include_router(admin.router)

add_pagination(app)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
