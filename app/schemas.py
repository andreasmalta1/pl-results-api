from pydantic import BaseModel
from datetime import date

# class TeamBase(BaseModel):
#     full_name: str
#     name: str
#     code: Optional[str]
#     nickname: Optional[str]
#     stadium: Optional[str]
#     competition: Optional[str]
#     website: Optional[str]
#     twitter_handle: Optional[str]
#     national_team: Optional[bool]
#     year_formed: Optional[int]
#     country: Optional[str]
#     location: Optional[str]
#     num_domestic_champions: Optional[int]


class TeamModel(BaseModel):
    id: int
    name: str
    alternative_name: str
    current_team: bool


class TeamCreate(TeamModel):
    pass


class TeamResponse(TeamModel):
    class Config:
        orm_mode = True


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
        orm_mode = True


class NationModel(BaseModel):
    id: int
    name: str

class NationCreate(NationModel):
    pass

class NationResponse(MatchModel):
    class Config:
        orm_mode = True


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
        orm_mode = True


class LastRowModel(BaseModel):
    last_row: int


class LastRowCreate(LastRowModel):
    pass


class LastRowResponse(LastRowModel):
    id: int

    class Config:
        orm_mode = True