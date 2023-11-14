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
        users = db.query(User).all()
        api_keys = [user.api_key for user in users]

    if api_key_header in api_keys:
        #     return api_keys[api_key_header]
        return api_key_header

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


def create_api_key():
    return secrets.token_urlsafe(16)
