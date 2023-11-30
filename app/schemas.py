from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class TeamModel(BaseModel):
    id: int
    name: str
    url: Optional[str]
    current_team: bool = False


class TeamCreate(TeamModel):
    pass


class TeamResponse(TeamModel):
    class Config:
        from_attributes = True


class MatchCreate(BaseModel):
    home_id: int
    home_score: int
    away_id: int
    away_score: int
    match_date: Optional[date] = date.today()
    season: Optional[str] = Field(min_length=9, max_length=9, default=None)


class MatchResponse(BaseModel):
    id: int
    home_team: Optional[TeamResponse]
    home_score: int
    away_team: Optional[TeamResponse]
    away_score: int
    match_date: Optional[date] = date.today()
    season: str

    class Config:
        from_attributes = True


class NationCreate(BaseModel):
    name: str


class NationResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ManagerCreate(BaseModel):
    nation_id: int
    name: str


class ManagerResponse(BaseModel):
    id: int
    name: str
    nation: Optional[NationResponse]

    class Config:
        from_attributes = True


class StintsCreate(BaseModel):
    manager_id: int
    team_id: int
    date_start: date
    date_end: Optional[date] = None
    current: bool = False


class StintsResponse(BaseModel):
    id: int
    manager: Optional[ManagerResponse]
    team: Optional[TeamResponse]
    date_start: date
    date_end: Optional[date] = None
    current: bool = False

    class Config:
        from_attributes = True
