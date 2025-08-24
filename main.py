import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from models import Animals
from schemas.animal import AnimalBase, AnimalOut, AnimalUpdate, AnimalInDB
from settings import get_db


app = FastAPI(docs_url="/")

@app.post("/animal", response_model=AnimalOut)
async def create_user(animal: AnimalBase, db: AsyncSession = Depends(get_db)):
    if animal.age < 0:
        raise HTTPException(status_code=400, detail="Age cannot be negative")
    new_animal = Animals(**animal.model_dump())
    db.add(new_animal)
    await db.commit()
    await db.refresh(new_animal)
    return new_animal


@app.get("/animals/", response_model=List[AnimalInDB])
async def get_all_animals(db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(Animals)
        result = await db.scalars(stmt)
        animals = result.all()
        return animals
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching animals: {str(e)}")


@app.put("/animals/{animal_id}", response_model=AnimalInDB)
async def update_animal(animal_id: int, animal_update: AnimalUpdate, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(Animals).where(Animals.id == animal_id)
        result = await db.scalars(stmt)
        animal = result.first()
        if not animal:
            raise HTTPException(status_code=404, detail="Animal not found")

        update_data = animal_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(animal, key, value)

        await db.commit()
        await db.refresh(animal)
        return animal
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating animal: {str(e)}")



@app.delete("/animals/{animal_id}")
async def delete_animal(animal_id: int, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(Animals).where(Animals.id == animal_id)
        result = await db.scalars(stmt)
        animal = result.first()
        if not animal:
            raise HTTPException(status_code=404, detail="Animal not found")

        await db.delete(animal)
        await db.commit()
        return {"message": "Animal deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting animal: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", port=8000, reload=True)
