from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.models import Condition
from schemas.schemas import ConditionOut

router = APIRouter()

@router.get("/", response_model=List[ConditionOut])
def get_all(category: Optional[str] = None, search: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Condition)
    if category:
        query = query.filter(Condition.category.ilike(f"%{category}%"))
    if search:
        query = query.filter(Condition.name.ilike(f"%{search}%"))
    return query.order_by(Condition.name).all()

@router.get("/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_db)):
    rows = db.query(Condition.category).distinct().all()
    return sorted([r[0] for r in rows])

@router.get("/{condition_id}", response_model=ConditionOut)
def get_one(condition_id: int, db: Session = Depends(get_db)):
    c = db.query(Condition).filter(Condition.id == condition_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Condition not found")
    return c
