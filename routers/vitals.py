from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.models import VitalRecord, User
from schemas.schemas import VitalIn, VitalOut
from auth_utils import get_current_user

router = APIRouter()

@router.post("/", response_model=VitalOut, status_code=201)
def save_vitals(payload: VitalIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = VitalRecord(user_id=current_user.id, **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[VitalOut])
def get_my_vitals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(VitalRecord).filter(VitalRecord.user_id == current_user.id).order_by(VitalRecord.recorded_at.desc()).all()

@router.delete("/{record_id}", status_code=204)
def delete_vital(record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = db.query(VitalRecord).filter(VitalRecord.id == record_id, VitalRecord.user_id == current_user.id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    db.delete(record)
    db.commit()
