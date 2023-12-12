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
from datetime import date
from pathlib import Path
from tempfile import NamedTemporaryFile
import os

from app.config import Settings
from app.database import get_db
from app.models import Manager, Nation, LastRow, Season, Stints, Team, User
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


@router.get("/new-manager", include_in_schema=False)
def new_manager(
    request: Request,
    user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    nations = db.query(Nation).order_by(Nation.name).all()
    return templates.TemplateResponse(
        "new_manager.html", {"request": request, "nations": nations}
    )


@router.post("/new-manager", include_in_schema=False)
def add_new_manager(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_token),
    manager_name: str = Form(...),
    nation: str = Form(...),
    manager_image: UploadFile = File(...),
):
    manager_dict = {"name": manager_name, "nation_id": nation}

    new_manager = Manager(**manager_dict)
    db.add(new_manager)
    db.commit()
    db.refresh(new_manager)

    temp = NamedTemporaryFile(delete=False, suffix=".png")
    try:
        try:
            contents = manager_image.file.read()
            with temp as temp_file:
                temp_file.write(contents)
        except Exception:
            raise HTTPException(status_code=500, detail="Error on uploading the file")
        finally:
            manager_image.file.close()

        bucket_upload.upload_to_bucket("managers", temp.name, new_manager.id)
        image_url = f"{BUCKET_HOST}/managers/{new_manager.id}.png"
        new_manager.image = image_url
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")
    finally:
        os.remove(temp.name)

    nations = db.query(Nation).order_by(Nation.name).all()
    return templates.TemplateResponse(
        "new_manager.html",
        {
            "request": request,
            "message": "New Manager added successfully",
            "nations": nations,
        },
    )


@router.get("/new-stint", include_in_schema=False)
def new_stint(
    request: Request,
    user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    teams = db.query(Team).order_by(Team.name).all()
    managers = db.query(Manager).order_by(Manager.name).all()
    return templates.TemplateResponse(
        "new_stint.html", {"request": request, "teams": teams, "managers": managers}
    )


@router.post("/new-stint", include_in_schema=False)
def add_new_stint(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_token),
    manager: str = Form(...),
    team: str = Form(...),
    date_start: date = Form(...),
):
    stint_dict = {
        "manager_id": manager,
        "team_id": team,
        "date_start": date_start,
        "current": True,
    }

    new_stint = Stints(**stint_dict)
    db.add(new_stint)
    db.commit()
    db.refresh(new_stint)

    teams = db.query(Team).order_by(Team.name).all()
    managers = db.query(Manager).order_by(Manager.name).all()
    return templates.TemplateResponse(
        "new_stint.html",
        {
            "request": request,
            "message": "New Stint added successfully",
            "teams": teams,
            "managers": managers,
        },
    )


@router.get("/end-stint", include_in_schema=False)
def end_stint(
    request: Request,
    user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    stints = (
        db.query(Stints).join(Manager).join(Team).filter(Stints.current == True).all()
    )
    return templates.TemplateResponse(
        "end_stint.html", {"request": request, "stints": stints}
    )


@router.post("/end-stint", include_in_schema=False)
def end_current_stint(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_token),
    stint: str = Form(...),
    date_end: date = Form(...),
):
    stint = db.query(Stints).filter(Stints.id == stint).first()

    stint.date_end = date_end
    stint.current = False
    db.commit()

    stints = (
        db.query(Stints).join(Manager).join(Team).filter(Stints.current == True).all()
    )
    return templates.TemplateResponse(
        "end_stint.html",
        {
            "request": request,
            "message": "Stint ended successfully",
            "stints": stints,
        },
    )


@router.get("/new-season", include_in_schema=False)
def new_season(
    request: Request,
    user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    current_teams = db.query(Team).filter(Team.current_team == True).all()
    non_current_teams = db.query(Team).filter(Team.current_team == False).all()

    return templates.TemplateResponse(
        "new_season.html",
        {
            "request": request,
            "current_teams": current_teams,
            "non_current_teams": non_current_teams,
        },
    )


@router.post("/new-season", include_in_schema=False)
async def start_new_season(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_token),
):
    form_data = await request.form()
    promoted_teams, relegated_teams = [], []

    for key, value in form_data.items():
        if value == "on":
            if "promoted" in key:
                promoted_teams.append(key.replace("promoted_", ""))
            if "releagted" in key:
                relegated_teams.append(key.replace("releagted_", ""))

    last_row = db.query(LastRow).filter(LastRow.id == 1).first()
    last_row.last_row = -1

    season = db.query(Season).filter(Season.id == 1).first()
    new_season = int(season.season.split("/")[0]) + 1
    season.season = f"{new_season}/{new_season + 1}"

    for team in promoted_teams:
        promoted_team = db.query(Team).filter(Team.id == team).first()
        promoted_team.current_team = True

    for team in relegated_teams:
        releagted_team = db.query(Team).filter(Team.id == team).first()
        releagted_team.current_team = False

    db.commit()

    current_teams = db.query(Team).filter(Team.current_team == True).all()
    non_current_teams = db.query(Team).filter(Team.current_team == False).all()
    return templates.TemplateResponse(
        "new_season.html",
        {
            "request": request,
            "message": "New season started successfully",
            "current_teams": current_teams,
            "non_current_teams": non_current_teams,
        },
    )
