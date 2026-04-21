from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from backendapi.schemas.user_schemas import (
    User_List,
    Userdb,
    UserSchema,
    UserSchemaPublic,
)

app = FastAPI(title='API Sitema Bancário')

database = []


@app.get('/')
def read_root():
    return {'msg': 'teste'}


@app.post(
    '/user/', status_code=HTTPStatus.CREATED, response_model=UserSchemaPublic
)
def create_user(user: UserSchema):
    user_with_id = Userdb(
        email=user.email,
        password=user.password,
        cpf=user.cpf,
        id=len(database) + 1,
    )
    database.append(user_with_id)
    return user_with_id


@app.get('/user/', status_code=HTTPStatus.OK, response_model=User_List)
def read_user():
    return {'users': database}


@app.put(
    '/user/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserSchemaPublic,
)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='user not found'
        )
    user_with_id = Userdb(
        email=user.email, password=user.password, cpf=user.cpf, id=user_id
    )
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/user/{user_id}', status_code=HTTPStatus.OK)
def delete_user(user_id: int):
    del database[user_id - 1]
    return {'msg': 'user deleted'}
