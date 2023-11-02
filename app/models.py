from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Team(Base):
    __tablename__ = "teams"

    # id = Column(Integer, primary_key=True, nullable=False)
    # full_name = Column(String, nullable=False)
    # name = Column(String, nullable=False)
    # code = Column(String, nullable=True)
    # nickname = Column(String, nullable=True)
    # stadium = Column(String, nullable=True)
    # competition = Column(String, nullable=True)
    # country = Column(String, nullable=True)
    # location = Column(String, nullable=True)
    # logo_url_small = Column(String, nullable=True)
    # logo_url_medium = Column(String, nullable=True)
    # logo_url_large = Column(String, nullable=True)
    # twitter_handle = Column(String, nullable=True)
    # website = Column(String, nullable=True)
    # national_team = Column(Boolean, server_default="False")
    # year_formed = Column(Integer, nullable=True)
    # player_record_appearances = Column(String, nullable=True)
    # record_num_appearances = Column(Integer, nullable=False, server_default=text("0"))
    # player_record_goals = Column(String, nullable=True)
    # record_num_goals = Column(Integer, nullable=False, server_default=text("0"))
    # num_domestic_champions = Column(Integer, nullable=False, server_default=text("0"))
    # created_at = Column(
    #     TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    # )

    # team name
    # team id
    # current


class Match(Base):
    __tablename__ = "users"

    # id = Column(Integer, primary_key=True, nullable=False)
    # email = Column(String, nullable=False, unique=True)
    # password = Column(String, nullable=False)
    # created_at = Column(
    #     TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    # )

    # id
    # home team - Foreign key
    # home score
    # away team - Foreign key
    # away score
    # date
    # season
    # date_added


class Manager(Base):
    pass
    # id  - fotmob id
    # manager name
    # nationality - Foreign Key
    # club - Foreign Key
    # date start
    # date end
    # current - boolean
    # date added


class Nations:
    pass
    # nation name
    # nation id -> fotmob id
    # date added


class LastRow:
    pass
    # last row
