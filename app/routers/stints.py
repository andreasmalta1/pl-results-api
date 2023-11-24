from fastapi import status, APIRouter, Depends, HTTPException, Response, Security
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_api_key, authorization_error
from app.database import get_db
from app.models import Stints, Manager, Team
import app.schemas as schemas


router = APIRouter(prefix="/api/stints", tags=["ManagerialStints"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.StintsResponse,
    include_in_schema=False,
)
def create_manager(
    stint: schemas.StintsCreate,
    api_key: str = Security(get_api_key),
    db: Session = Depends(get_db),
):
    if not api_key:
        authorization_error()

    new_stint = Stints(**stint.model_dump())
    manager_id = new_stint.manager_id
    team_id = new_stint.team

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


# @router.get("/", response_model=Page[schemas.ManagerResponse])
# def get_managers(
#     nation: int | None = None,
#     api_key: str = Security(get_api_key),
#     db: Session = Depends(get_db),
# ):
#     managers_query = select(Manager).order_by(Manager.id)
#     if nation:
#         managers_query = managers_query.filter(Manager.nationality == nation)

#     return paginate(db, managers_query)


# @router.get("/{id}", response_model=schemas.ManagerResponse)
# def get_manager(
#     id: int,
#     api_key: str = Security(get_api_key),
#     db: Session = Depends(get_db),
# ):
#     manager = db.query(Manager).filter(Manager.id == id).first()

#     if not manager:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Manager with id {id} was not found",
#         )

#     return manager


# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
# def delete_manager(
#     id: int,
#     api_key: str = Security(get_api_key),
#     db: Session = Depends(get_db),
# ):
#     if not api_key:
#         authorization_error()

#     manager_query = db.query(Manager).filter(Manager.id == id)
#     manager = manager_query.first()

#     if manager == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Manager with id {id} was not found",
#         )

#     manager_query.delete(synchronize_session=False)
#     db.commit()

#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.put("/{id}", response_model=schemas.ManagerResponse, include_in_schema=False)
# def update_manager(
#     id: int,
#     updated_manager: schemas.ManagerCreate,
#     api_key: str = Security(get_api_key),
#     db: Session = Depends(get_db),
# ):
#     if not api_key:
#         authorization_error()

#     manager_query = db.query(Manager).filter(Manager.id == id)
#     manager = manager_query.first()

#     if manager == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Manager with id {id} was not found",
#         )

#     updated_manager = updated_manager.model_dump()
#     nation_id = updated_manager.get("nationality")

#     nation = db.query(Nation).filter(Nation.id == nation_id).first()

#     if not nation:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Nation with id {nation_id} was not found",
#         )

#     manager_query.update(updated_manager, synchronize_session=False)
#     db.commit()

#     return manager_query.first()
