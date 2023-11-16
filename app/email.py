import os
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_USERNAME"),
    MAIL_PORT=os.getenv("MAIL_PORT"),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME="Andreas Calleja",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_email(subject, body):
    message = MessageSchema(
        subject=subject,
        recipients=["andreascalleja@gmail.com"],
        body=body,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return
