from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from core.database import get_db
from models import Routine, RoutineStep, RoutineCompletion, StepCompletion, User
from schemas.completion import RoutineCompletionResponse, StepCompletionCreate, StepCompletionResponse

router = APIRouter(prefix='/completions', tags=['completions'])

@router.post("/routine/{routine_id}", response_model=RoutineCompletionResponse)
def complete_routine(routine_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Marquer une routine complète comme terminée
    """
    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    total_steps = len(routine.steps)
    points_earned = total_steps * 5

    db_completion = RoutineCompletion(
        user_id=user_id,
        routine_id=routine_id,
        points_earned=points_earned,
        all_steps_completed=True
    )
    db.add(db_completion)

    user.points += points_earned
    user.current_streak += 1
    
    db.commit()
    db.refresh(db_completion)

    return db_completion

@router.post("/step/{step_id}", response_model=StepCompletionResponse)
def complete_step(step_id: int, completion_data: StepCompletionCreate, db: Session = Depends(get_db)):
    """
    Marquer une étape comme terminée
    """

    step = db.query(RoutineStep).filter(RoutineStep.id == step_id).first()
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")

    db_step_completion = StepCompletion(
        step_id=step_id,
        time_taken=completion_data.time_taken
    )
    db.add(db_step_completion)
    db.commit()
    db.refresh(db_step_completion)

    return db_step_completion
