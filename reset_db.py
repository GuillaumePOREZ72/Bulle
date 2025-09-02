from core.database import engine, Base
from models import User, Routine, RoutineStep, RoutineCompletion, StepCompletion

Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)

print("Tables recréées avec succès!")