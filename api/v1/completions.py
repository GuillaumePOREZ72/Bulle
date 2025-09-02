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

@router.get("/user/{user_id}/stats")
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    """
    Récupère les statistiques d'un utilisateur
    """

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    total_completions = db.query(RoutineCompletion).filter(RoutineCompletion.user_id == user_id).count()

    # Routines terminées cette semaine (exemple simple)
    from datetime import timedelta
    week_ago = datetime.now() - timedelta(days=7)
    week_completions = db.query(RoutineCompletion).filter(RoutineCompletion.user_id == user_id,
     RoutineCompletion.completed_at >= week_ago
    ).count()

    return {
        "user_id": user_id,
        "username": user.username,
        "points": user.points,
        "current_streak": user.current_streak,
        "total_routines_completed": total_completions,
        "routines_this_week": week_completions,
        "level": user.points // 100 + 1 # Niveau basé sur les points
    }

    @router.get("/user/{user_id}/history", response_model=List[RoutineCompletionResponse])
    def get_completion_history(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
        """
        Récupère l'historique des routines terminées par un utilisateur
        """

        completions = db.query(RoutineCompletion).filter(RoutineCompletion.user_id == user_id).order_by(RoutineCompletion.completed_at.desc()).limit(limit).all()
        
        return completions