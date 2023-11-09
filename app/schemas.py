import os
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class TeamModel(BaseModel):
    id: int
    name: str
    alternative_name: str
    current_team: bool = False


class TeamCreate(TeamModel):
    pass


class TeamResponse(TeamModel):
    class Config:
        from_attributes = True


class MatchModel(BaseModel):
    home_id: int
    home_score: int
    away_id: int
    away_score: int
    match_date: Optional[date] = date.today()
    season: Optional[str] = Field(
        min_length=9, max_length=9, default=os.getenv("CURRENT_SEASON")
    )


class MatchCreate(MatchModel):
    pass


class MatchResponse(MatchModel):
    id: int

    class Config:
        from_attributes = True


class NationModel(BaseModel):
    id: int
    name: str


class NationCreate(NationModel):
    pass


class NationResponse(NationModel):
    class Config:
        from_attributes = True


class ManagerModel(BaseModel):
    name: str
    fotmob_id: int
    nationality: int
    team: int
    date_start: date
    date_end: date
    current: bool


class ManagerCreate(ManagerModel):
    pass


class ManagerResponse(ManagerModel):
    id: int

    class Config:
        from_attributes = True


class LastRowModel(BaseModel):
    last_row: int


class LastRowCreate(LastRowModel):
    pass


class LastRowResponse(LastRowModel):
    id: int

    class Config:
        from_attributes = True
