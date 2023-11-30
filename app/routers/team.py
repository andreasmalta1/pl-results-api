from fastapi import status, APIRouter, Depends, HTTPException, Response, Security
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_api_key, authorization_error
from app.database import get_db
from app.models import Team
from app.schemas import TeamCreate, TeamResponse


router = APIRouter(prefix="/api/teams", tags=["Teams"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TeamResponse,
    include_in_schema=False,
)
def create_team(
    team: TeamCreate,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    if not api_key:
        authorization_error()

    new_team = Team(**team.model_dump())
    if db.query(Team).filter(Team.id == new_team.id).first() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team with id {new_team.id} already exists",
        )

    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return new_team


@router.get("/", response_model=Page[TeamResponse])
def get_teams(
    search: str | None = None,
    current: bool | None = None,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    teams_query = select(Team).order_by(Team.id)
    if current != None:
        teams_query = teams_query.filter(Team.current_team == current)

    if search != None:
        teams_query = teams_query.filter(Team.name.ilike("%" + search + "%"))

    return paginate(db, teams_query)


@router.get("/{id}", response_model=TeamResponse)
def get_team(
    id: int, api_key: str = Security(get_api_key), db: Session = Depends(get_db)
):
    team = db.query(Team).filter(Team.id == id).first()

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )

    return team


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_team(
    id: int,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    if not api_key:
        authorization_error()

    team_query = db.query(Team).filter(Team.id == id)
    team = team_query.first()

    if team == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )

    team_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=TeamResponse, include_in_schema=False)
def update_team(
    id: int,
    updated_team: TeamCreate,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    if not api_key:
        authorization_error()

    team_query = db.query(Team).filter(Team.id == id)
    team = team_query.first()

    if team == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )

    team_query.update(updated_team.model_dump(), synchronize_session=False)
    db.commit()

    return team_query.first()
