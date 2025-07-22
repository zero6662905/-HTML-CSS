from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from Participant import Note
from settings import get_db
import uvicorn

app = FastAPI(debug=True, docs_url="/")


@app.get("/")
async def home():
    return {}


@app.post("/participants/")
async def post_participants(name: str, email: str, event: str, age: int, db: AsyncSession = Depends(get_db)):
    if not name or not event:
        raise HTTPException(status_code=400, detail="Name and event must not be empty")
    if not (12 <= age <= 120):
        raise HTTPException(status_code=400, detail="Age must be between 12 and 120")

    try:
        db_participant = Note(name=name, email=email, event=event, age=age)
        db.add(db_participant)
        await db.commit()
        await db.refresh(db_participant)
        return {"name": name, "email": email, "event": event, "age": age}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating participant: {str(e)}")


@app.get("/participants/event/{event_name}/")
async def get_participants(event_name: str, db: AsyncSession = Depends(get_db)):
    participants = await db.execute(select(Note).filter(Note.event == event_name))
    participants = participants.scalars().all()
    if not participants:
        raise HTTPException(status_code=404, detail="No participants found for this event")
    return [{"id": p.id, "name": p.name, "email": p.email, "event": p.event, "age": p.age} for p in participants]


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)