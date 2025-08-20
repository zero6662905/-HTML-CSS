import uvicorn
from fastapi import Depends, FastAPI, Query
from sqlalchemy.ext.asyncio import AsyncSession

from models import Animals
from settings import get_db
from schemas.animal import AnimalBase, AnimalOut


app = FastAPI(docs_url="/")


@app.get("/hello")
async def hello_user(username: str = Query("Anonymous",  description="Ім'я користувача")):
    return {"message": f"hello {username}"}

@app.post("/user", response_model=AnimalOut)
async def create_user(animal: AnimalBase, db: AsyncSession = Depends(get_db)):
    new_animal = Animals(**animal.model_dump())
    db.add(new_animal)
    await db.commit()
    await db.refresh(new_animal)
    return new_animal


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", port=8000, reload=True)
