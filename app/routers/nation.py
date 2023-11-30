from fastapi import status, APIRouter, Depends, HTTPException, Response, Security
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_api_key, authorization_error
from app.database import get_db
from app.models import Nation
from app.schemas import NationCreate, NationResponse


router = APIRouter(prefix="/api/nations", tags=["Nations"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=NationResponse,
    include_in_schema=False,
)
def create_nation(
    nation: NationCreate,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    if not api_key:
        authorization_error()

    new_nation = Nation(**nation.model_dump())
    db.add(new_nation)
    db.commit()
    db.refresh(new_nation)

    return new_nation


@router.get("/", response_model=Page[NationResponse])
def get_nations(
    search: str | None = None,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    nation_query = select(Nation).order_by(Nation.id)
    if search != None:
        nation_query = nation_query.filter(Nation.name.ilike("%" + search + "%"))

    return paginate(db, nation_query)


@router.get("/{id}", response_model=NationResponse)
def get_nation(
    id: int, api_key: str = Security(get_api_key), db: Session = Depends(get_db)
):
    nation = db.query(Nation).filter(Nation.id == id).first()

    if not nation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nation with id {id} was not found",
        )

    return nation


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_nation(
    id: int,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    if not api_key:
        authorization_error()

    nation_query = db.query(Nation).filter(Nation.id == id)
    nation = nation_query.first()

    if nation == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nation with id {id} was not found",
        )

    nation_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=NationResponse, include_in_schema=False)
def update_nation(
    id: int,
    updated_nation: NationCreate,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    if not api_key:
        authorization_error()

    nation_query = db.query(Nation).filter(Nation.id == id)
    nation = nation_query.first()

    if nation == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nation with id {id} was not found",
        )

    nation_query.update(updated_nation.model_dump(), synchronize_session=False)
    db.commit()

    return nation_query.first()
