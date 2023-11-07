from fastapi import status, APIRouter, HTTPException, Response, Depends, Request
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from pydantic import create_model
import random

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


@router.get("/", response_model=List[schemas.TeamResponse])
def get_teams(
    db: Session = Depends(get_db),
    limit: int = 10,
):
    results = db.query(models.Team).order_by(models.Team.id).limit(limit).all()
    return results


@router.get("/{id}", response_model=schemas.TeamResponse)
def get_team(id: int, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == id).first()

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )

    return team


# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
# def delete_team(
#     request: Request,
#     id: int,
#     current_user: int = Depends(oauth2.get_current_user),
#     db: Session = Depends(get_db),
# ):
#     if current_user.id != 1:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=f"Unauthorized action",
#         )

#     team_query = db.query(models.Team).filter(models.Team.id == id)
#     team = team_query.first()

#     if team == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Team with id {id} was not found",
#         )

#     team_query.delete(synchronize_session=False)
#     db.commit()

#     post_request(db, "teams", request)

#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.put("/{id}", response_model=schemas.TeamResponse, include_in_schema=False)
# def update_team(
#     request: Request,
#     id: int,
#     updated_team: schemas.TeamCreate,
#     current_user: int = Depends(oauth2.get_current_user),
#     db: Session = Depends(get_db),
# ):
#     if current_user.id != 1:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=f"Unauthorized action",
#         )

#     team_query = db.query(models.Team).filter(models.Team.id == id)
#     team = team_query.first()

#     if team == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Team with id {id} was not found",
#         )

#     team_query.update(updated_team.dict(), synchronize_session=False)
#     db.commit()

#     post_request(db, "teams", request)

#     return team_query.first()
