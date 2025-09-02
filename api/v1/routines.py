from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from models import Routine, RoutineStep
from schemas.routine import RoutineCreate, RoutineResponse, RoutineStepResponse

router = APIRouter(prefix='/routines', tags=['routines'])

@router.post("/", response_model=RoutineResponse)
def create_routine(routine: RoutineCreate, db: Session = Depends(get_db)):
    """
    Créé une nouvelle routine avec ses étapes
    """

    db_routine = Routine(
        user_id=routine.user_id, 
        name=routine.name, 
        description=routine.description, 
        icon=routine.icon, 
        color=routine.color, 
        start_time=routine.start_time, 
        estimated_duration=routine.estimated_time
    )
    db.add(db_routine)
    db.commit()
    db.refresh(db_routine)

    for step_data in routine.steps:
        db_step = RoutineStep(
            routine_id=db_routine.id, 
            **step_data.dict()
        )
        db.add(db_step)
        
    db.commit()
    db.refresh(db_routine)

    return db_routine

@router.get("/{routine_id}", response_model=RoutineResponse)
def get_routine(routine_id: int, db: Session = Depends(get_db)):
    """
    Récupère une routine par son ID, avec toutes ses étapes
    """
    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    
    return routine

@router.get("/", response_model=List[RoutineResponse])
def list_routines(user_id: int = None, db: Session = Depends(get_db)):
    """
    Liste toutes les routines d'un utilisateur
    """
    if user_id is None:
        routines = db.query(Routine).filter(Routine.is_active == True).all()
    else:
        routines = db.query(Routine).filter(Routine.user_id == user_id, Routine.is_active == True).all()
        
    return routines