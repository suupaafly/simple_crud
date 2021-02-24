import typing as t

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

import database
import schemas


class UserNotExist(Exception):
    pass


class UpdateUserError(Exception):
    pass


def user_get(db: Session, user_id: str) -> database.User:
    try:
        return db.query(database.User).filter(database.User.id == user_id).one()
    except NoResultFound:
        raise UserNotExist


def user_find_by_email(db: Session, email: str) -> t.Optional[database.User]:
    return db.query(database.User).filter(database.User.email == email).one_or_none()


def user_create(db: Session, user: schemas.UserData) -> database.User:
    db_user = database.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def user_modify(db: Session, user_id: str, user: schemas.UserData):
    try:
        db_user = db.query(database.User).filter(database.User.id == user_id).one()
    except NoResultFound:
        raise UserNotExist

    try:
        db_user.firstname = user.firstname
        db_user.lastname = user.lastname
        db_user.email = user.email
        db.commit()
    except IntegrityError as e:
        raise UpdateUserError from e


def user_delete(db: Session, user_id: str):
    try:
        db_user = db.query(database.User).filter(database.User.id == user_id).one()
    except NoResultFound:
        raise UserNotExist

    db.delete(db_user)
    db.commit()
