from fastapi import status, APIRouter, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from pathlib import Path

from app.config import Settings
from app.oauth2 import oauth_login


BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

router = APIRouter(prefix="/admin")


@router.get("/login", include_in_schema=False)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", include_in_schema=False)
def login(
    request: Request,
    email: EmailStr = Form(...),
    password: str = Form(...),
):
    response = RedirectResponse("/", status.HTTP_302_FOUND)
    try:
        access_token = oauth_login(response, email, password)
    except HTTPException:
        return templates.TemplateResponse(
            "login.html", {"request": request, "message": "not logged in"}
        )
    response = RedirectResponse("/", status.HTTP_302_FOUND)
    response.set_cookie(
        key=Settings.COOKIE_NAME, value=f"Bearer {access_token}", httponly=True
    )
    return templates.TemplateResponse(
        "login.html", {"request": request, "message": "logged in"}
    )


# @router.get("/logout")
# def logout():
#     response = RedirectResponse(url="/")
#     response.delete_cookie(Settings.COOKIE_NAME)
#     return response
