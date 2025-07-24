from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr, constr
from typing import List
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.Participant import Note
from settings import get_db

app = FastAPI(debug=True, docs_url="/")


class ParticipantCreate(BaseModel):
    name: constr(min_length=1)
    email: EmailStr
    event: constr(min_length=1)
    age: int


@app.get("/")
async def home():
    return {}


@app.post("/participants/", response_model=ParticipantCreate)
async def post_participants(participant: ParticipantCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_participant = Note(
            name=participant.name,
            email=participant.email,
            event=participant.event,
            age=participant.age
        )
        db.add(db_participant)
        await db.commit()
        await db.refresh(db_participant)
        return participant
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating participant: {str(e)}")


@app.get("/participants/event/{event_name}/", response_model=List[ParticipantCreate])
async def get_participants(event_name: str, db: AsyncSession = Depends(get_db)):
    participants = await db.execute(select(Note).filter(Note.event == event_name))
    participants = participants.scalars().all()
    if not participants:
        raise HTTPException(status_code=404, detail="No participants found for this event")
    return participants


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)