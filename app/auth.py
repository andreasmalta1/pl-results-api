from fastapi import HTTPException, status, Security
from fastapi.security import APIKeyHeader
from contextlib import contextmanager
import secrets

from .database import get_db
from .models import User

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def get_api_key(api_key_header: str = Security(api_key_header)):
    """Retrieve and validate an API key from the query parameters or HTTP header.

    Args:
        api_key_query: The API key passed as a query parameter.
        api_key_header: The API key passed in the HTTP header.

    Returns:
        The validated API key.

    Raises:
        HTTPException: If the API key is invalid or missing.
    """

    with contextmanager(get_db)() as db:
        user = db.query(User).filter(User.api_key == api_key_header).first()
        if not user:
            authorization_error()

        user.num_visits = user.num_visits + 1
        db.commit()

        return user.admin


def create_api_key():
    return secrets.token_urlsafe(16)


def authorization_error():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
