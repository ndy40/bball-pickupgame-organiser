from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from services import user_service

from ._responses import UserModel, TokenModel


user_route = APIRouter(tags=['user'])


@user_route.post('/register', response_model=UserModel)
async def register_user(username: str):
    user = await user_service.register(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error registering')

    return UserModel.from_orm(user)


@user_route.post('/login')
async def login(username: str) -> str:
    token = await user_service.authenticate(username)

    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid auth')

    return TokenModel(token=token)




