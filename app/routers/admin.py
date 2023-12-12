from fastapi import (
    status,
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    Response,
    UploadFile,
)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import EmailStr
from pathlib import Path
from tempfile import NamedTemporaryFile
import os

from app.config import Settings
from app.database import get_db
from app.models import Nation, Team, User
from app.oauth2 import oauth_login, get_current_user_from_token
from app.utils import bucket_upload


BASE_DIR = Path(__file__).resolve().parent.parent
BUCKET_HOST = os.getenv("BUCKET_HOST")

templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

router = APIRouter(prefix="/admin")


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
    if not email:
        return templates.TemplateResponse(
            "login.html", {"request": request, "message": "No email inputted"}
        )

    if not password:
        return templates.TemplateResponse(
            "login.html", {"request": request, "message": "No password inputted"}
        )

    response = RedirectResponse("/admin", status.HTTP_302_FOUND)
    try:
        access_token = oauth_login(response, email, password)
    except HTTPException:
        return templates.TemplateResponse(
            "login.html", {"request": request, "message": "Login Unsuccessful"}
        )
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie(Settings.COOKIE_NAME)
    return response


@router.get("/", include_in_schema=False)
def admin_page(request: Request, user: User = Depends(get_current_user_from_token)):
    return templates.TemplateResponse("admin.html", {"request": request})


@router.get("/new-team", include_in_schema=False)
def new_team(request: Request, user: User = Depends(get_current_user_from_token)):
    return templates.TemplateResponse("new_team.html", {"request": request})


@router.post("/new-team", include_in_schema=False)
def add_new_team(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_token),
    team_name: str = Form(...),
    current: bool = Form(False),
    team_image: UploadFile = File(...),
):
    team_dict = {"name": team_name, "current_team": current}

    new_team = Team(**team_dict)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    temp = NamedTemporaryFile(delete=False, suffix=".png")
    try:
        try:
            contents = team_image.file.read()
            with temp as temp_file:
                temp_file.write(contents)
        except Exception:
            raise HTTPException(status_code=500, detail="Error on uploading the file")
        finally:
            team_image.file.close()

        bucket_upload.upload_to_bucket("clubs", temp.name, new_team.id)
        image_url = f"{BUCKET_HOST}/clubs/{new_team.id}.png"
        new_team.logo = image_url
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong")
    finally:
        os.remove(temp.name)

    return templates.TemplateResponse(
        "new_team.html", {"request": request, "message": "New Team added successfully"}
    )


@router.get("/new-nation", include_in_schema=False)
def new_nation(request: Request, user: User = Depends(get_current_user_from_token)):
    return templates.TemplateResponse("new_nation.html", {"request": request})


@router.post("/new-nation", include_in_schema=False)
def add_new_nation(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_token),
    nation_name: str = Form(...),
    nation_image: UploadFile = File(...),
):
    nation_dict = {"name": nation_name}

    new_nation = Nation(**nation_dict)
    db.add(new_nation)
    db.commit()
    db.refresh(new_nation)

    temp = NamedTemporaryFile(delete=False, suffix=".png")
    try:
        try:
            contents = nation_image.file.read()
            with temp as temp_file:
                temp_file.write(contents)
        except Exception:
            raise HTTPException(status_code=500, detail="Error on uploading the file")
        finally:
            nation_image.file.close()

        bucket_upload.upload_to_bucket("nations", temp.name, new_nation.id)
        image_url = f"{BUCKET_HOST}/nations/{new_nation.id}.png"
        new_nation.flag = image_url
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")
    finally:
        os.remove(temp.name)

    return templates.TemplateResponse(
        "new_nation.html",
        {"request": request, "message": "New Nation added successfully"},
    )
