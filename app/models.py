from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, DATE

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

    id = Column(Integer, primary_key=True, nullable=False)
    home_id = Column(Integer, ForeignKey("teams.id"))
    home_score = Column(Integer, server_default="0")
    away_id = Column(Integer, ForeignKey("teams.id"))
    away_score = Column(Integer, server_default="")
    date = Column(DATE, server_default="CURRENT_DATE")
    season = Column(String(9), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Nations:
    __tablename__ = "nations"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Manager(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    fotmob_id = Column(String, nullable=False, unique=True)
    nationality = Column(Integer, ForeignKey("nations.id"), nullable=False)
    team = Column(Integer, ForeignKey("team.id"), nullable=False)
    date_start = Column(DATE, nullable=False)
    date_start = Column(DATE)
    curent = Column(Boolean, server_default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class LastRow:
    pass
    # last row
