from fastapi import status, APIRouter, HTTPException, Response, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

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
    season: str | None = None,
    team: int | None = None,
):
    match_query = select(models.Match).order_by(models.Match.id)
    if season:
        match_query = match_query.filter(models.Match.season == season)
    if team:
        match_query = match_query.filter(
            or_(models.Match.home_id == team, models.Match.away_id == team)
        )

    return paginate(db, match_query)


@router.get("/{id}", response_model=schemas.MatchResponse)
def get_match(id: int, db: Session = Depends(get_db)):
    match = db.query(models.Match).filter(models.Match.id == id).first()

    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {id} was not found",
        )

    return match


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_match(
    id: int,
    db: Session = Depends(get_db),
):
    match_query = db.query(models.Match).filter(models.Match.id == id)
    match = match_query.first()

    if match == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {id} was not found",
        )

    match_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.MatchResponse, include_in_schema=False)
def update_match(
    id: int,
    updated_match: schemas.MatchCreate,
    db: Session = Depends(get_db),
):
    match_query = db.query(models.Match).filter(models.Match.id == id)
    match = match_query.first()

    if match == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {id} was not found",
        )

    updated_match = updated_match.model_dump()
    home_id = updated_match.get("home_id")
    away_id = updated_match.get("away_id")

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

    match_query.update(updated_match, synchronize_session=False)
    db.commit()

    return match_query.first()
