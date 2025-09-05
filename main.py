from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from pathlib import Path
import uuid
import mimetypes
import jwt
from passlib.context import CryptContext
from typing import List
from settings import api_config, get_db
from models import UserDB
from schemas import PhotoResponse, User, Token
import uvicorn

app = FastAPI(docs_url="/")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

MAX_FILE_SIZE = 5 * 1024 * 1024

SECRET_KEY = api_config.SECRET_KEY
ALGORITHM = "HS512"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_user(db: AsyncSession, username: str):
    result = await db.execute(select(UserDB).filter(UserDB.username == username))
    return result.scalars().first()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = await get_user(db, username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@app.post("/register")
async def register_user(user: User, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    db_user = UserDB(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return {"message": "User created successfully"}

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

def is_valid_image(file: UploadFile) -> bool:
    mime_type, _ = mimetypes.guess_type(file.filename)
    return mime_type in ["image/jpeg", "image/png"]

@app.post("/photos/upload", response_model=PhotoResponse)
async def upload_photo(file: UploadFile = File(...), current_user: UserDB = Depends(get_current_user)):
    if not is_valid_image(file):
        raise HTTPException(status_code=400, detail="Only JPEG or PNG files are allowed")

    file_size = await file.read()
    if len(file_size) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 5MB limit")

    unique_filename = f"{uuid.uuid4()}{Path(file.filename).suffix}"
    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as f:
        f.write(file_size)

    photo_url = f"/photos/{unique_filename}"

    return PhotoResponse(
        url=photo_url,
        uploaded_at=datetime.fromtimestamp(file_path.stat().st_mtime)
    )

@app.get("/photos/list", response_model=List[PhotoResponse])
async def list_photos(current_user: UserDB = Depends(get_current_user)):
    photos = []
    for file_path in UPLOAD_DIR.glob("*"):
        if file_path.is_file():
            photos.append(PhotoResponse(
                url=f"/photos/{file_path.name}",
                uploaded_at=datetime.fromtimestamp(file_path.stat().st_mtime)
            ))

    photos.sort(key=lambda x: x.uploaded_at, reverse=True)
    return photos

@app.get("/photos/{filename}")
async def get_photo(filename: str, current_user: UserDB = Depends(get_current_user)):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Photo not found")

    return FileResponse(file_path)

if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", port=5050, reload=True)
