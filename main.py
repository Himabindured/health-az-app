from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from database import engine, Base
from routers import auth, conditions, vitals, users, ai, rag
from seed import seed_conditions
import os

app = FastAPI(title="Health A-Z API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
seed_conditions()

app.include_router(auth.router,       prefix="/auth",       tags=["Auth"])
app.include_router(users.router,      prefix="/users",      tags=["Users"])
app.include_router(conditions.router, prefix="/conditions", tags=["Conditions"])
app.include_router(vitals.router,     prefix="/vitals",     tags=["Vitals"])
app.include_router(ai.router,         prefix="/ai",         tags=["AI"])
app.include_router(rag.router,        tags=["RAG"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/app")
def serve_frontend():
    html_path = os.path.join(BASE_DIR, "index.html")
    if not os.path.exists(html_path):
        return {"error": f"index.html not found at {html_path}"}
    return FileResponse(html_path)

@app.get("/")
def root():
    return {"message": "Health A-Z API is running! Go to /app"}
