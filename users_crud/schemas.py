import pydantic


class UserData(pydantic.BaseModel):
    firstname: str
    lastname: str
    email: pydantic.EmailStr


class User(UserData):
    id: int

    class Config:
        orm_mode = True
