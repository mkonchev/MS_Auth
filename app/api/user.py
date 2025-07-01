from fastapi import APIRouter, HTTPException
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.services.user_service import UserService, UserResponse

router = APIRouter(prefix="/users")


@router.post("/register", response_model=UserResponse)
async def register(user: UserRegister):
    try:
        return UserService.register(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin):
    token = UserService.authenticate(user.email, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
