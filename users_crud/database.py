import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

engine = sa.create_engine(settings.db_uri)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    firstname = sa.Column(sa.Text)
    lastname = sa.Column(sa.Text)
    email = sa.Column(sa.String, unique=True)
