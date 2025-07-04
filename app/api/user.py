from fastapi import APIRouter, HTTPException, Depends
# from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.schemas import User as schemas
from app.services.user_service import UserService
from app.db.database import SessionLocal

router = APIRouter(prefix="/users")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


# def get_current_user(
#         token: str = Depends(oauth2_scheme),
#         db: Session = Depends(get_db)
# ):
#     service = UserService(db)
#     user = service.info(token)
#     return user


@router.post("/register", response_model=schemas.UserResponse)
def register(
    user: schemas.UserRegister,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    try:
        return service.register(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=schemas.TokenResponse)
def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    token = service.authenticate(user.email, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login_username", response_model=schemas.TokenResponse)
def login_username(
    user: schemas.UserLoginUsername,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    token = service.authenticate_username(user.username, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
def get_info(
    # token: str = Depends(oauth2_scheme),
    token: str,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    user = service.info(token)
    if not token:
        raise HTTPException(status_code=401, detail="smth wrong")
    return user


# @router.put("/", response_model=schemas.PasswordUpdate)
# def change_password(
#     user: schemas.UserLogin,
#     new_password: str,
#     db: Session = Depends(get_db)
# ):
#     service = UserService(db)
#     user = service.change_password(
#         user.email,
#         user.password,
#         new_password
#     )
#     return user


# @router.post("/me", response_model=schemas.UserResponse)
# def info(
#     current_user: schemas.UserResponse = Depends(oauth2_scheme)
# ):
#     return current_user
