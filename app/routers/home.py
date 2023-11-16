from fastapi import status, APIRouter, Depends, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from pathlib import Path
from sqlalchemy.orm import Session
from random import randbytes
import hashlib


from app.database import get_db
from app.auth import create_api_key
from app.email import send_email
import app.models as models

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

router = APIRouter()


@router.get("/", include_in_schema=False)
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/register", include_in_schema=False)
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", include_in_schema=False)
async def create_new_user(
    request: Request, email: EmailStr = Form(...), db: Session = Depends(get_db)
):
    if not email:
        return templates.TemplateResponse(
            "register.html", {"request": request, "error": "No email inputted"}
        )

    user = db.query(models.User).filter(models.User.email == email).first()

    if user:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "You are already registered for this service",
            },
        )

    token = randbytes(10)
    hashedCode = hashlib.sha256()
    hashedCode.update(token)
    verification_code = hashedCode.hexdigest()

    new_user = models.User(
        email=email,
        api_key=None,
        admin=False,
        is_verified=False,
        verification_code=verification_code,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    url = f"{request.url.scheme}://{request.client.host}:{request.url.port}/verifyemail/{token.hex()}"
    subject = "PL Results API Registration"
    body = f"""Welcome to the PL Results API. Please follow the link belowto active your account and receive your API Key. Please store your key in a safe and secure place
            <a href="{url}">Click here!</a>
        """
    await send_email(subject, body)

    return templates.TemplateResponse(
        "register.html", {"request": request, "error": "email sent"}
    )


@router.get("/verifyemail/{token}", include_in_schema=False)
def verify_me(request: Request, token: str, db: Session = Depends(get_db)):
    hashedCode = hashlib.sha256()
    hashedCode.update(bytes.fromhex(token))
    verification_code = hashedCode.hexdigest()

    user = (
        db.query(models.User)
        .filter(models.User.verification_code == verification_code)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid verification code or account already verified",
        )

    api_key = create_api_key()
    user.is_verified = True
    user.api_key = api_key
    user.verification_code = None

    db.commit()

    return templates.TemplateResponse(
        "index.html", {"request": request, "api_key": api_key}
    )
