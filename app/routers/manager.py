from fastapi import status, APIRouter, Depends, HTTPException, Response, Security
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_api_key
import app.schemas as schemas
import app.models as models


router = APIRouter(prefix="/api/managers", tags=["Managers"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ManagerResponse,
    include_in_schema=False,
)
def create_manager(
    manager: schemas.ManagerCreate,
    db: Session = Depends(get_db),
):
    new_manager = models.Manager(**manager.model_dump())
    team_id = new_manager.team
    nation_id = new_manager.nationality

    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    nation = db.query(models.Nation).filter(models.Nation.id == nation_id).first()

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {team_id} was not found",
        )

    if not nation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nation with id {nation_id} was not found",
        )

    if manager.current == True:
        new_manager.date_end = None

    if manager.current == False:
        if not manager.date_end:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Managers which are not current must have an date end",
            )
        if manager.date_start >= manager.date_end:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Manager start date must be before manager end date",
            )

    db.add(new_manager)
    db.commit()
    db.refresh(new_manager)

    return new_manager


@router.get("/", response_model=Page[schemas.ManagerResponse])
def get_managers(
    db: Session = Depends(get_db),
    current: bool | None = None,
    nation: int | None = None,
    team: int | None = None,
    api_key: str = Security(get_api_key),
):
    managers_query = select(models.Manager).order_by(models.Manager.id)
    if current != None:
        managers_query = managers_query.filter(models.Manager.current == current)

    if nation:
        managers_query = managers_query.filter(models.Manager.nationality == nation)

    if team:
        managers_query = managers_query.filter(models.Manager.team == team)

    return paginate(db, managers_query)


@router.get("/{id}", response_model=schemas.ManagerResponse)
def get_manager(id: int, db: Session = Depends(get_db)):
    manager = db.query(models.Manager).filter(models.Manager.id == id).first()

    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manager with id {id} was not found",
        )

    return manager


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_manager(
    id: int,
    db: Session = Depends(get_db),
):
    manager_query = db.query(models.Manager).filter(models.Manager.id == id)
    manager = manager_query.first()

    if manager == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manager with id {id} was not found",
        )

    manager_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.ManagerResponse, include_in_schema=False)
def update_manager(
    id: int,
    updated_manager: schemas.ManagerCreate,
    db: Session = Depends(get_db),
):
    manager_query = db.query(models.Manager).filter(models.Manager.id == id)
    manager = manager_query.first()

    if manager == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manager with id {id} was not found",
        )

    updated_manager = updated_manager.model_dump()
    team_id = updated_manager.get("team")
    nation_id = updated_manager.get("nationality")

    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    nation = db.query(models.Nation).filter(models.Nation.id == nation_id).first()

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {team_id} was not found",
        )

    if not nation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nation with id {nation_id} was not found",
        )

    if updated_manager.get("current") == True:
        updated_manager["date_end"] = None

    if updated_manager.get("current") == False:
        if not updated_manager.get("date_end"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Managers which are not current must have an date end",
            )

        if updated_manager.get("date_start") >= updated_manager.get("date_end"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Manager start date must be before manager end date",
            )

    manager_query.update(updated_manager, synchronize_session=False)
    db.commit()

    return manager_query.first()
