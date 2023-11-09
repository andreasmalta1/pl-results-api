from fastapi import status, APIRouter, HTTPException, Response, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
import app.schemas as schemas
import app.models as models


router = APIRouter(prefix="/api/nations", tags=["Nations"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.NationResponse,
    include_in_schema=False,
)
def create_nation(
    nation: schemas.NationCreate,
    db: Session = Depends(get_db),
):
    new_nation = models.Nation(**nation.model_dump())
    db.add(new_nation)
    db.commit()
    db.refresh(new_nation)

    return new_nation


@router.get("/", response_model=Page[schemas.NationResponse])
def get_nations(
    db: Session = Depends(get_db),
):
    nation_query = select(models.Nation).order_by(models.Nation.id)
    return paginate(db, nation_query)


@router.get("/{id}", response_model=schemas.NationResponse)
def get_nation(id: int, db: Session = Depends(get_db)):
    nation = db.query(models.Nation).filter(models.Nation.id == id).first()

    if not nation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nation with id {id} was not found",
        )

    return nation


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_nation(
    id: int,
    db: Session = Depends(get_db),
):
    nation_query = db.query(models.Nation).filter(models.Nation.id == id)
    nation = nation_query.first()

    if nation == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nation with id {id} was not found",
        )

    nation_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.NationResponse, include_in_schema=False)
def update_nation(
    id: int,
    updated_nation: schemas.NationCreate,
    db: Session = Depends(get_db),
):
    nation_query = db.query(models.Nation).filter(models.Nation.id == id)
    nation = nation_query.first()

    if nation == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nation with id {id} was not found",
        )

    nation_query.update(updated_nation.model_dump(), synchronize_session=False)
    db.commit()

    return nation_query.first()
