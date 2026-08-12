"""
routers/rag.py

New endpoint: POST /rag/ask
Takes a user's health question, retrieves the most relevant conditions
from the DB, and asks Gemini to answer using only that retrieved context
(so answers stay grounded in your own data, not the model's general
knowledge).

Install first:
    pip install google-generativeai

Set your API key as an environment variable (match whatever name you
already used in routers/ai.py, e.g.):
    GEMINI_API_KEY=your-key-here
"""

import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import google.generativeai as genai

from database import get_db  # adjust if your dependency is named differently
from rag_utils import retrieve_relevant_conditions, _to_text

load_dotenv()

router = APIRouter(prefix="/rag", tags=["rag"])

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-flash-latest")


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest, db: Session = Depends(get_db)):
    # 1. Retrieve relevant conditions from your DB
    conditions = retrieve_relevant_conditions(payload.question, db, top_k=3)

    # 2. Build context block from retrieved conditions
    context_blocks = []
    for c in conditions:
        context_blocks.append(
            f"Name: {_to_text(getattr(c, 'name', ''))}\n"
            f"Category: {_to_text(getattr(c, 'category', ''))}\n"
            f"Overview: {_to_text(getattr(c, 'overview', ''))}\n"
            f"Symptoms: {_to_text(getattr(c, 'symptoms', ''))}\n"
            f"Treatment: {_to_text(getattr(c, 'treatment', ''))}"
        )
    context_text = "\n\n---\n\n".join(context_blocks)

    # 3. Ask Claude, grounded strictly in the retrieved context
    system_prompt = (
        "You are a health information assistant for the Health A-Z app. "
        "Answer the user's question using ONLY the context provided below. "
        "If the context doesn't contain enough information to answer, say so "
        "and recommend the user consult a doctor. Do not give diagnoses or "
        "treatment advice beyond what's in the context. Keep answers concise."
    )

    user_message = f"Context:\n{context_text}\n\nQuestion: {payload.question}"

    full_prompt = f"{system_prompt}\n\n{user_message}"

    response = gemini_model.generate_content(full_prompt)
    answer_text = response.text

    return AskResponse(
        answer=answer_text,
        sources=[getattr(c, "name", "") for c in conditions],
    )
