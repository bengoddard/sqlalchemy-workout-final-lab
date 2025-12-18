#!/usr/bin/env python3

from app import app
from models import *
from datetime import date

with app.app_context():

    WorkoutExercises.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    ex1 = Exercise(name="Pushups", category="Chest", equipment_needed=False)
    ex2 = Exercise(name="Squats", category="Legs", equipment_needed=False)
    ex3 = Exercise(name="Bench Press", category="Chest", equipment_needed=True)
    ex4 = Exercise(name="Deadlift", category="Back", equipment_needed=True)

    db.session.add_all([ex1, ex2, ex3, ex4])
    db.session.commit()

    w1 = Workout(date=date(2025, 12, 18), duration_minutes=45, notes="Great morning session")
    w2 = Workout(date=date(2025, 12, 19), duration_minutes=30, notes="Quick lunch workout")

    db.session.add_all([w1, w2])
    db.session.commit()

    we1 = WorkoutExercises(workout=w1, exercise=ex1, sets=3, reps=15)
    we2 = WorkoutExercises(workout=w1, exercise=ex2, sets=4, reps=12)
    we3 = WorkoutExercises(workout=w2, exercise=ex3, sets=5, reps=5, duration_seconds=300)

    db.session.add_all([we1, we2, we3])
    db.session.commit()