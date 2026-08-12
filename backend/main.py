from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import engine, Base
from routers import auth, conditions, vitals, users
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

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(conditions.router, prefix="/conditions", tags=["Conditions"])
app.include_router(vitals.router, prefix="/vitals", tags=["Vitals"])

# Serve frontend from ../frontend/
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.get("/app", response_class=FileResponse)
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/")
def root():
    return {"message": "Health A-Z API running! Open /app to use the app."}
