from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: str
    cpf: int


class UserSchemaPublic(BaseModel):
    email: EmailStr
    id: int


class Userdb(UserSchema):
    id: int


class User_List(BaseModel):
    users: list[UserSchemaPublic]
