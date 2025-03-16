from pydantic import BaseModel
from typing import List
from app.models.models import TrainingFrequency

class MyTrainingExerciseCreate(BaseModel):
    name: str
    sets: int
    repetitions: int


class MyTrainingCreate(BaseModel):
    name: str
    training_frequency: TrainingFrequency
    exercises: List[MyTrainingExerciseCreate]

class AddExercisesToTraining(BaseModel):
    exercises: List[MyTrainingExerciseCreate]

class TrainingExerciseOut(BaseModel):
    exercise_name: str
    sets: int
    repetitions: int

class GettingMyTraining(BaseModel):
    name: str
    training_frequency: str
    my_training_exercises: List[TrainingExerciseOut]




