import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()
engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URL"))
