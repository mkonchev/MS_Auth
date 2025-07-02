from app.models.user import fake_users, fake_usernames
from app.schemas.user import UserRegister, UserResponse
from app.core.security import verify_password, create_access_token
from app.core.security import get_password_hash, get_from_token


class UserService:
    @staticmethod
    def register(user: UserRegister):
        if user.email in fake_users:
            raise ValueError("Email already registered")

        if user.username in fake_usernames:
            raise ValueError("username already registered")

        hashed_password = get_password_hash(user.password)
        fake_users[user.email] = {
            "email": user.email,
            "username": user.username,
            "hashed_password": hashed_password
        }
        fake_usernames[user.username] = {
            "email": user.email,
            "username": user.username,
            "hashed_password": hashed_password
        }
        return UserResponse(**user.model_dump())

    @staticmethod
    def authenticate(email: str, password: str):
        user = fake_users.get(email)
        if not user or not verify_password(password, user["hashed_password"]):
            return None
        return create_access_token({"sub": email})

    @staticmethod
    def info(token: str):
        user = get_from_token(token)
        return user
