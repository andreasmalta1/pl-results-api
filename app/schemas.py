from pydantic import BaseModel, Field, model_serializer
from datetime import date
from typing import Optional, Dict, Any


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
    season: Optional[str] = Field(min_length=9, max_length=9, default=None)

    class Config:
        from_attributes = True


class NationModel(BaseModel):
    name: str


class NationCreate(NationModel):
    pass


class NationResponse(NationModel):
    id: int

    class Config:
        from_attributes = True


class ManagerModel(BaseModel):
    name: str


class ManagerCreate(ManagerModel):
    nation_id: int


class ManagerResponse(ManagerModel):
    id: int
    nation: Optional[NationResponse]

    class Config:
        from_attributes = True


class StintsModel(BaseModel):
    date_start: date
    date_end: Optional[date] = None
    current: bool = False


class StintsCreate(StintsModel):
    manager_id: int
    team_id: int


class StintsResponse(StintsModel):
    id: int
    manager: Optional[ManagerResponse]
    team: Optional[TeamResponse]

    class Config:
        from_attributes = True
