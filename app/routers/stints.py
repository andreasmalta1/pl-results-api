from fastapi import status, APIRouter, Depends, HTTPException, Response, Security
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import date

from app.auth import get_api_key, authorization_error
from app.database import get_db
from app.models import Stints, Manager, Team
from app.schemas import StintsCreate, StintsResponse


router = APIRouter(prefix="/api/stints", tags=["ManagerialStints"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=StintsResponse,
    include_in_schema=False,
)
def create_stint(
    stint: StintsCreate,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    if not api_key:
        authorization_error()

    new_stint = Stints(**stint.model_dump())
    manager_id = new_stint.manager_id
    team_id = new_stint.team_id

    manager = db.query(Manager).filter(Manager.id == manager_id).first()
    team = db.query(Team).filter(Team.id == team_id).first()

    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manager with id {manager_id} was not found",
        )

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {team_id} was not found",
        )

    if stint.current == True:
        new_stint.date_end = None

    if stint.current == False:
        if not stint.date_end:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Managerial stints which are not current must have an date end",
            )
        if stint.date_start >= stint.date_end:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Manager stint start date must be before manager end date",
            )

    db.add(new_stint)
    db.commit()
    db.refresh(new_stint)

    return new_stint


@router.get("/", response_model=Page[StintsResponse])
def get_stints(
    current: bool | None = None,
    manager: int | None = None,
    team: int | None = None,
    date_start: date | None = None,
    date_end: date | None = None,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    stints_query = select(Stints).order_by(Stints.id)
    if current != None:
        stints_query = stints_query.filter(Stints.current == current)
    if manager:
        stints_query = stints_query.filter(Stints.manager_id == manager)
    if team:
        stints_query = stints_query.filter(Stints.team_id == team)
    if date_start and date_end:
        stints_query = stints_query.filter(
            Stints.match_date >= date_start, Stints.match_date <= date_end
        )

    return paginate(db, stints_query)


@router.get("/{id}", response_model=StintsResponse)
def get_stint(
    id: int,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    stint = db.query(Stints).filter(Stints.id == id).first()

    if not stint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint with id {id} was not found",
        )

    return stint


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_stint(
    id: int,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    if not api_key:
        authorization_error()

    stint_query = db.query(Stints).filter(Stints.id == id)
    stint = stint_query.first()

    if stint == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint with id {id} was not found",
        )

    stint_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=StintsResponse, include_in_schema=False)
def update_stint(
    id: int,
    updated_stint: StintsCreate,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    if not api_key:
        authorization_error()

    stint_query = db.query(Stints).filter(Stints.id == id)
    stint = stint_query.first()

    if stint == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stint with id {id} was not found",
        )

    updated_stint = updated_stint.model_dump()
    manager_id = updated_stint.get("manager_id")
    team_id = updated_stint.get("team_id")

    manager = db.query(Manager).filter(Manager.id == manager_id).first()
    team = db.query(Team).filter(Team.id == team_id).first()

    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manager with id {manager_id} was not found",
        )

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {team_id} was not found",
        )

    if updated_stint.get("current") == True:
        updated_stint["date_end"] = None

    if updated_stint.get("current") == False:
        if not updated_stint.get("date_end"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Managerial stints which are not current must have an date end",
            )
        if updated_stint.get("date_start") >= updated_stint.get("date_end"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Manager stint start date must be before manager end date",
            )

    stint_query.update(updated_stint, synchronize_session=False)
    db.commit()

    return stint_query.first()
