from fastapi import APIRouter, Form, Depends, Request, Security
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from pathlib import Path
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import create_api_key
import app.models as models

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

