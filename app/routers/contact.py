from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from pathlib import Path
from sqlalchemy.orm import Session


from app.database import get_db
from app.send_email import send_email

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

router = APIRouter()


@router.get("/contact", include_in_schema=False)
def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@router.post("/contact", include_in_schema=False)
async def contact_form(
    request: Request,
    name: str = Form(...),
    email: EmailStr = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db),
):
    if not name:
        return templates.TemplateResponse(
            "contact.html", {"request": request, "message": "No name inputted"}
        )

    if not email:
        return templates.TemplateResponse(
            "contact.html", {"request": request, "message": "No email inputted"}
        )

    if not message:
        return templates.TemplateResponse(
            "contact.html", {"request": request, "message": "No message inputted"}
        )

    subject = "PL Results API - New Message"
    body = f"""<h1>New Message From PL Results API</h1>
                <h3>Name: {name}</h3>
                <h3>Email: {email}</h3>
                <br>
                <p>{message}</p>"""
    await send_email(subject, body)

    return templates.TemplateResponse(
        "contact.html", {"request": request, "message": "Your email has been sent"}
    )
