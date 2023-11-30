from fastapi import status, APIRouter, Depends, HTTPException, Response, Security
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_api_key, authorization_error
from app.database import get_db
from app.models import Nation, Manager
from app.schemas import ManagerCreate, ManagerResponse


router = APIRouter(prefix="/api/managers", tags=["Managers"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ManagerResponse,
    include_in_schema=False,
)
def create_manager(
    manager: ManagerCreate,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    if not api_key:
        authorization_error()

    new_manager = Manager(**manager.model_dump())
    nation_id = new_manager.nation_id

    nation = db.query(Nation).filter(Nation.id == nation_id).first()

    if not nation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nation with id {nation_id} was not found",
        )

    db.add(new_manager)
    db.commit()
    db.refresh(new_manager)

    return new_manager


@router.get("/", response_model=Page[ManagerResponse])
def get_managers(
    search: str | None = None,
    nation: int | None = None,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    managers_query = select(Manager).order_by(Manager.id)
    if search != None:
        managers_query = managers_query.filter(Manager.name.ilike("%" + search + "%"))

    if nation:
        managers_query = managers_query.filter(Manager.nation_id == nation)

    return paginate(db, managers_query)


@router.get("/{id}", response_model=ManagerResponse)
def get_manager(
    id: int,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    manager = db.query(Manager).filter(Manager.id == id).first()

    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manager with id {id} was not found",
        )

    return manager


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_manager(
    id: int,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    if not api_key:
        authorization_error()

    manager_query = db.query(Manager).filter(Manager.id == id)
    manager = manager_query.first()

    if manager == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manager with id {id} was not found",
        )

    manager_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=ManagerResponse, include_in_schema=False)
def update_manager(
    id: int,
    updated_manager: ManagerCreate,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    if not api_key:
        authorization_error()

    manager_query = db.query(Manager).filter(Manager.id == id)
    manager = manager_query.first()

    if manager == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manager with id {id} was not found",
        )

    updated_manager = updated_manager.model_dump()
    nation_id = updated_manager.get("nation_id")

    nation = db.query(Nation).filter(Nation.id == nation_id).first()

    if not nation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nation with id {nation_id} was not found",
        )

    manager_query.update(updated_manager, synchronize_session=False)
    db.commit()

    return manager_query.first()
