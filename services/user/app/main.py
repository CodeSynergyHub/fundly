from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserCreate, UserResponse
from app.crud import create_user, get_user_by_username
from app.auth import verify_password, create_access_token, SECRET_KEY, ALGORITHM
from app.database import get_db


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)


@app.post("/register", response_model=UserResponse)
async def register_user(
    user_create: UserCreate, db: AsyncSession = Depends(get_db)
) -> any:
    db_user = await get_user_by_username(db, user_create.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = await create_user(db, user_create)
    return new_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> any:
    user = await get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(subject={"username": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        user = await get_user_by_username(db, username)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


@app.get("/me")
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user
