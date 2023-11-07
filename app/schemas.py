from pydantic import BaseModel
from datetime import date
from typing import Optional, Union


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
    date: date
    season: str


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


class NationResponse(MatchModel):
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
