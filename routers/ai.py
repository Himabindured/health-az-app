from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx
import os

router = APIRouter()

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

class AskRequest(BaseModel):
    question: str
    condition: Optional[str] = None

@router.post("/ask")
async def ask_ai(payload: AskRequest):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")
    if payload.condition:
        prompt = f'You are a health information assistant. The user is reading about "{payload.condition}". Answer this question in 3-5 sentences: {payload.question}. Always recommend consulting a healthcare professional.'
    else:
        prompt = f'You are a health information assistant. Answer this health question in 3-5 sentences: {payload.question}. Always recommend consulting a qualified healthcare professional.'
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(
                f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"maxOutputTokens": 500}
                }
            )
            data = res.json()
            if res.status_code != 200:
                raise HTTPException(status_code=500, detail=data.get("error", {}).get("message", "AI request failed"))
            answer = data["candidates"][0]["content"]["parts"][0]["text"]
            return {"answer": answer}
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="AI request timed out.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))