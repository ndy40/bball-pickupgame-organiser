from datetime import datetime, timedelta, timezone

import jwt

from db.model import User
from db.repository import user_repo
from config import settings

from .exceptions import UserAlreadyExistsError


class JwtUtils:
    @staticmethod
    async def generate_token(claims: dict) -> str:
        required_fields = ("sub", "aud")

        if not set(required_fields).issubset(claims):
            raise ValueError("missing required claims sub or aud")

        current_time = datetime.now(tz=timezone.utc)
        claims["iat"] = current_time
        claims["exp"] = timedelta(days=7) + current_time

        return jwt.encode(claims, settings.SECRET, algorithm="HS256")

    @staticmethod
    async def decode(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.SECRET,
                audience="players",
                algorithms="hS256",
                options={"require": ["exp", "iat", "sub", "aud"]},
            )
            return isinstance(token, dict)
        except jwt.InvalidTokenError:
            pass

    @staticmethod
    async def get_claim(token: str, attr: str):
        claim = JwtUtils.decode(token)
        return claim.get(attr, None)


async def authenticate(username: str) -> str or None:
    result = await user_repo.find_username(username=username)

    if isinstance(result, (User,)):
        user = result
        user.last_login = datetime.now(tz=timezone.utc)
        await user_repo.update(user)
        return await JwtUtils.generate_token({"sub": user.username, "aud": "players"}) if user else None


async def register(username: str) -> User or None:
    username_min_len = 3
    if len(username) <= username_min_len:
        return None

    user = await user_repo.find_username(username=username)

    if user:
        raise UserAlreadyExistsError

    new_user = User(username=username)
    return await user_repo.save(new_user)



