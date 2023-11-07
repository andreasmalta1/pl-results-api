from fastapi import status, APIRouter, HTTPException, Response, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
import app.schemas as schemas
import app.models as models


router = APIRouter(prefix="/api/matches", tags=["Matches"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MatchResponse,
    include_in_schema=False,
)
def create_match(
    match: schemas.MatchCreate,
    db: Session = Depends(get_db),
):
    new_match = models.Match(**match.model_dump())
    home_id = new_match.home_id
    away_id = new_match.away_id

    home_team = db.query(models.Team).filter(models.Team.id == home_id).first()
    away_team = db.query(models.Team).filter(models.Team.id == away_id).first()

    if not home_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Home team with id {home_id} was not found",
        )

    if not away_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Away team with id {away_id} was not found",
        )

    db.add(new_match)
    db.commit()
    db.refresh(new_match)

    return new_match


@router.get("/", response_model=Page[schemas.MatchResponse])
def get_matches(
    db: Session = Depends(get_db),
    # current: bool | None = None,
):
    matches = db.query(models.Match).order_by(models.Match.id).all()
    return paginate(matches)


# @router.get("/{id}", response_model=schemas.TeamResponse)
# def get_team(id: int, db: Session = Depends(get_db)):
#     team = db.query(models.Team).filter(models.Team.id == id).first()

#     if not team:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Team with id {id} was not found",
#         )

#     return team


# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
# def delete_team(
#     id: int,
#     db: Session = Depends(get_db),
# ):
#     team_query = db.query(models.Team).filter(models.Team.id == id)
#     team = team_query.first()

#     if team == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Team with id {id} was not found",
#         )

#     team_query.delete(synchronize_session=False)
#     db.commit()

#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.put("/{id}", response_model=schemas.TeamResponse, include_in_schema=False)
# def update_team(
#     id: int,
#     updated_team: schemas.TeamCreate,
#     db: Session = Depends(get_db),
# ):
#     team_query = db.query(models.Team).filter(models.Team.id == id)
#     team = team_query.first()

#     if team == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Team with id {id} was not found",
#         )

#     team_query.update(updated_team.dict(), synchronize_session=False)
#     db.commit()

#     return team_query.first()
