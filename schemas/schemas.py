from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# --- Auth ---
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- User ---
class UserOut(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    class Config:
        from_attributes = True

# --- Conditions ---
class ConditionOut(BaseModel):
    id: int
    name: str
    category: str
    overview: str
    symptoms: List[str]
    severity: int
    treatment: str
    class Config:
        from_attributes = True

# --- Vitals ---
class VitalIn(BaseModel):
    heart_rate: Optional[float] = None
    systolic_bp: Optional[float] = None
    diastolic_bp: Optional[float] = None
    temperature: Optional[float] = None
    spo2: Optional[float] = None
    notes: Optional[str] = None

class VitalOut(VitalIn):
    id: int
    user_id: int
    recorded_at: datetime
    class Config:
        from_attributes = True
