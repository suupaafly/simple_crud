import logging

import fastapi
from sqlalchemy import orm

import crud
import database
import schemas
from config import settings

log = logging.getLogger('user_crud')

app = fastapi.FastAPI()

database.Base.metadata.create_all(bind=database.engine)


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/ping')
def ping():
    return 'pong'


@app.get('/health')
def ping():
    return {'status': 'OK'}


@app.get('/config')
def get_config():
    return settings.dict()


@app.post('/user', response_model=schemas.User)
def user_create(user: schemas.UserData, db: orm.Session = fastapi.Depends(get_db)):
    db_user = crud.user_find_by_email(db, email=user.email)
    if db_user:
        raise fastapi.HTTPException(status_code=400, detail="Email already registered")

    return crud.user_create(db=db, user=user)


@app.get('/user/{user_id}')
def user_get(user_id: str, db: orm.Session = fastapi.Depends(get_db)):
    try:
        return crud.user_get(db, user_id)
    except crud.UserNotExist:
        raise fastapi.HTTPException(status_code=404, detail='User not found')


@app.delete('/user/{user_id}')
def user_delete(user_id: str, db: orm.Session = fastapi.Depends(get_db)):
    try:
        crud.user_delete(db, user_id)
    except crud.UserNotExist:
        raise fastapi.HTTPException(status_code=404, detail='User not found')

    return 'OK'


@app.put('/user/{user_id}')
def user_update(user_id: str, user: schemas.UserData, db: orm.Session = fastapi.Depends(get_db)):
    try:
        crud.user_modify(db, user_id, user)
    except crud.UserNotExist:
        raise fastapi.HTTPException(status_code=404, detail='User not found')
    except crud.UpdateUserError:
        log.exception('User update error')
        raise fastapi.HTTPException(status_code=400, detail='User update error')

    return 'OK'
