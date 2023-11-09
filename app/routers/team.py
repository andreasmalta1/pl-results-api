from fastapi import status, APIRouter, HTTPException, Response, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
import app.schemas as schemas
import app.models as models


router = APIRouter(prefix="/api/teams", tags=["Teams"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.TeamResponse,
    include_in_schema=False,
)
def create_team(
    team: schemas.TeamCreate,
    db: Session = Depends(get_db),
):
    new_team = models.Team(**team.model_dump())
    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return new_team


@router.get("/", response_model=Page[schemas.TeamResponse])
def get_teams(
    db: Session = Depends(get_db),
    current: bool | None = None,
):
    teams_query = select(models.Team).order_by(models.Team.id)
    if current != None:
        teams_query = teams_query.filter(models.Team.current_team == current)

    return paginate(db, teams_query)


@router.get("/{id}", response_model=schemas.TeamResponse)
def get_team(id: int, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == id).first()

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )

    return team


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_team(
    id: int,
    db: Session = Depends(get_db),
):
    team_query = db.query(models.Team).filter(models.Team.id == id)
    team = team_query.first()

    if team == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )

    team_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.TeamResponse, include_in_schema=False)
def update_team(
    id: int,
    updated_team: schemas.TeamCreate,
    db: Session = Depends(get_db),
):
    team_query = db.query(models.Team).filter(models.Team.id == id)
    team = team_query.first()

    if team == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )

    team_query.update(updated_team.model_dump(), synchronize_session=False)
    db.commit()

    return team_query.first()
