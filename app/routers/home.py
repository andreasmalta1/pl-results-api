from fastapi import APIRouter, Form, Depends, Request, Security
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from pathlib import Path
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_api_key, create_api_key
import app.models as models
import app.schemas as schemas

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

router = APIRouter()


@router.get("/", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post(path="/")
def home_create(
    request: Request, email: EmailStr = Form(...), db: Session = Depends(get_db)
):
    if not email:
        return templates.TemplateResponse(
            "index.html", {"request": request, "error": "No email inputted"}
        )

    users = db.query(models.User).all()
    emails = [user.email for user in users]
    if email in emails:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "You are already registered for this service",
            },
        )

    api_key = create_api_key()

    new_user = models.User(email=email, api_key=api_key, admin=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return templates.TemplateResponse(
        "index.html", {"request": request, "api_key": api_key}
    )


# Show API key
# Forgotten API key -> update
# Maybe send email as confirmation
# Hash API key?
# HTTPS & API Keys


# def get_managers(
#     db: Session = Depends(get_db),
#     current: bool | None = None,
#     nation: int | None = None,
#     team: int | None = None,
#     api_key: str = Security(get_api_key),
# ):
#     managers_query = select(models.Manager).order_by(models.Manager.id)
#     if current != None:
#         managers_query = managers_query.filter(models.Manager.current == current)

#     if nation:
#         managers_query = managers_query.filter(models.Manager.nationality == nation)

#     if team:
#         managers_query = managers_query.filter(models.Manager.team == team)

#     return paginate(db, managers_query)
