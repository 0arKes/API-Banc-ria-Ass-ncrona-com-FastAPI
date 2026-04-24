from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from backendapi.database import create_session
from backendapi.models.user_models import User
from backendapi.schemas.token_schemas import Token
from backendapi.schemas.user_schemas import (
    UserList,
    UserSchema,
    UserSchemaPublic,
    UserUpdate,
)
from backendapi.security import (
    creat_access_token,
    get_current_user,
    get_password_hash,
    verify_password_hash,
)

app = FastAPI(title='API Sitema Bancário')


@app.get('/')
def read_root():
    return {'msg': 'teste'}


@app.post('/token/', response_model=Token)
def get_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(create_session),
):
    user_from_db = session.scalar(
        select(User).where(User.email == form_data.username)
    )
    if not user_from_db:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, detail='Incorrect email or password'
        )

    if not verify_password_hash(form_data.password, user_from_db.password):
        raise HTTPException(
            HTTPStatus.NOT_FOUND, detail='Incorrect email or password'
        )

    access_token = creat_access_token(data={'sub': user_from_db.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@app.post(
    '/user/', status_code=HTTPStatus.CREATED, response_model=UserSchemaPublic
)
def create_user(user: UserSchema, session: Session = Depends(create_session)):
    user_from_db = session.scalar(
        select(User).where((User.email == user.email) | (User.cpf == user.cpf))
    )
    if user_from_db:
        raise HTTPException(
            HTTPStatus.CONFLICT, detail='email or cpf already exists'
        )

    user_data = User(
        email=user.email,
        password=get_password_hash(user.password),
        cpf=user.cpf,
    )
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data


@app.get('/user/', status_code=HTTPStatus.OK, response_model=UserList)
def read_user(
    skip: int = 0, limit: int = 10, session: Session = Depends(create_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.put(
    '/user/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserSchemaPublic,
)
def update_user(
    user_id: int,
    user: UserUpdate,
    session: Session = Depends(create_session),
    current_user: User = Depends(get_current_user),
):

    if current_user.id != user_id:
        raise HTTPException(
            HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    if not current_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='user not found'
        )

    current_user.password = get_password_hash(user.password)
    session.commit()
    session.refresh(current_user)
    return current_user


@app.delete('/user/{user_id}', status_code=HTTPStatus.OK)
def delete_user(
    user_id: int,
    session: Session = Depends(create_session),
    current_user: User = Depends(get_current_user),
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    if not current_user:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='User not found')

    session.delete(current_user)
    session.commit()

    return {'msg': 'user deleted'}
