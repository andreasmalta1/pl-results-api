from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, DATE

try:
    from database import Base
except ModuleNotFoundError:
    from .database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    alternative_name = Column(String, nullable=False)
    current_team = Column(Boolean, server_default="False")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    home_id = Column(Integer, ForeignKey("teams.id"))
    home_score = Column(Integer, server_default="0")
    away_id = Column(Integer, ForeignKey("teams.id"))
    away_score = Column(Integer, server_default="0")
    match_date = Column(DATE, server_default="now()")
    season = Column(String(9), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class LastRow(Base):
    __tablename__ = "lastrow"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    last_row = Column(Integer, primary_key=True, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    api_key = Column(String, unique=True)
    admin = Column(Boolean, server_default="False")
    is_verified = Column(Boolean, server_default="False")
    verification_code = Column(String, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Season(Base):
    __tablename__ = "season"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    season = Column(String(9), nullable=False)
