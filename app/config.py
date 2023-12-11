import os


class Settings:
    SECRET_KEY = os.getenv("JWT_KEY")
    ALGORITHM = os.getenv("HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRY"))
    COOKIE_NAME = os.getenv("JWT_NAME")


settings = Settings()
