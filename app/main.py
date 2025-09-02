from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from core.database import get_db, engine, Base
from api.v1 import users, routines
from models import User, Routine, RoutineStep, RoutineCompletion, StepCompletion

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bulle API - Routine TDAH",
    description="API Backend pour l'application Bulle",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/v1")
app.include_router(routines.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Bulle API is running! 🎯"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        result = db.execute(text('SELECT 1')).scalar()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

