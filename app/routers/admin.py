from fastapi import status, APIRouter, Form, HTTPException, Request
from fastapi import Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from pathlib import Path

from app.config import Settings
from app.oauth2 import oauth_login


BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

router = APIRouter(prefix="/admin")


@router.get("/", include_in_schema=False)
def test_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/login", include_in_schema=False)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", include_in_schema=False)
async def login(
    request: Request,
    response: Response,
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
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie(Settings.COOKIE_NAME)
    return response
