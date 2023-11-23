import os
from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional
from contextlib import contextmanager


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
    season: Optional[str] = Field(min_length=9, max_length=9, default=None)


class MatchCreate(MatchModel):
    pass


class MatchResponse(MatchModel):
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


class UserBase(BaseModel):
    email: EmailStr
    admin: bool
    is_verified: bool


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    pass

    class Config:
        from_attributes = True
