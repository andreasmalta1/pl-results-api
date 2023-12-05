from fastapi import APIRouter, Depends, Form, Request, Security
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from pathlib import Path
from sqlalchemy.orm import Session
from random import randbytes
import hashlib


from app.database import get_db
from app.auth import get_api_key
from app.send_email import send_email
from app.models import User

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

router = APIRouter(prefix="/admin")


@router.get("/", include_in_schema=False)
def admin_home_page(
    request: Request,
    api_key: str = Security(get_api_key),
):
    if not api_key:
        return templates.TemplateResponse(
            "admin_home.html", {"request": request, "message": "Invalid API Key"}
        )

    return templates.TemplateResponse("index.html", {"request": request})
