from fastapi import status, APIRouter, Depends, HTTPException, Response, Security
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, or_
from sqlalchemy.orm import Session, aliased
from datetime import date

from app.auth import get_api_key, authorization_error
from app.database import get_db
from app.models import Match, Team, Season
from app.schemas import MatchCreate, MatchResponse


router = APIRouter(prefix="/api/matches", tags=["Matches"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=MatchResponse,
    include_in_schema=False,
)
def create_match(
    match: MatchCreate,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    if not api_key:
        authorization_error()

    new_match = Match(**match.model_dump())
    home_id = new_match.home_id
    away_id = new_match.away_id

    home_team = db.query(Team).filter(Team.id == home_id).first()
    away_team = db.query(Team).filter(Team.id == away_id).first()

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

    if not new_match.season:
        current_season = db.query(Season).first().season
        new_match.season = current_season

    db.add(new_match)
    db.commit()
    db.refresh(new_match)

    return new_match


@router.get("/", response_model=Page[MatchResponse])
def get_matches(
    season: str | None = None,
    date_start: date | None = None,
    date_end: date | None = None,
    team: int | None = None,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    home_team_alias = aliased(Team)
    away_team_alias = aliased(Team)

    match_query = (
        select(Match)
        .join(home_team_alias, Match.home_team)
        .join(away_team_alias, Match.away_team)
        .order_by(Match.id)
    )
    if season:
        match_query = match_query.filter(Match.season == season)
    if team:
        match_query = match_query.filter(
            or_(Match.home_id == team, Match.away_id == team)
        )
    if date_start and date_end:
        match_query = match_query.filter(
            Match.match_date >= date_start, Match.match_date <= date_end
        )

    return paginate(db, match_query)


@router.get("/{id}", response_model=MatchResponse)
def get_match(
    id: int, api_key: str = Security(get_api_key), db: Session = Depends(get_db)
):
    home_team_alias = aliased(Team)
    away_team_alias = aliased(Team)

    match_query = (
        select(Match, home_team_alias, away_team_alias)
        .join(home_team_alias, Match.home_team)
        .join(away_team_alias, Match.away_team)
        .filter(Match.id == id)
    )

    match = db.execute(match_query).fetchone()

    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {id} was not found",
        )

    match_info, home_team, away_team = match
    match = dict(
        match_info.__dict__, home_team=home_team.__dict__, away_team=away_team.__dict__
    )

    return match


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_match(
    id: int,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    if not api_key:
        authorization_error()

    match_query = db.query(Match).filter(Match.id == id)
    match = match_query.first()

    if match == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {id} was not found",
        )

    match_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=MatchResponse, include_in_schema=False)
def update_match(
    id: int,
    updated_match: MatchCreate,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    if not api_key:
        authorization_error()

    match_query = db.query(Match).filter(Match.id == id)
    match = match_query.first()

    if match == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {id} was not found",
        )

    updated_match = updated_match.model_dump()
    home_id = updated_match.get("home_id")
    away_id = updated_match.get("away_id")

    home_team = db.query(Team).filter(Team.id == home_id).first()
    away_team = db.query(Team).filter(Team.id == away_id).first()

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
