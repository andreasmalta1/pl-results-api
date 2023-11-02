from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.routers import match, team

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

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(match.router)
app.include_router(team.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
