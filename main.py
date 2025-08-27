from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bulle API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Bulle API is running!"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        result = db.execute(text('SELECT 1')).scalar()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

