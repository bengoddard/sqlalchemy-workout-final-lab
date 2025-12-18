from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from marshmallow import Schema, fields
db = SQLAlchemy()

# Define Models here
class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)

    workout_exercises = db.relationship('WorkoutExercises', back_populates='exercise')

    workouts = db.relationship("Workout", secondary="workout_exercises", back_populates='exercises')

    def __repr__(self):
        return f"<Exercise(id={self.id}, name={self.name}, category={self.category}, equipment_needed={self.equipment_needed}m)>"

    @validates('name')
    def validate_name(self, key, Exname):
        if not Exname:
            raise ValueError("Name must be present.")
        duplicate_name = db.session.query(Exercise.id).filter_by(name = Exname).first()
        if duplicate_name is not None:
            raise ValueError("Name must be unique.")
        return Exname

class ExerciseSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    category = fields.String()
    equipment_needed = fields.Boolean()

    workout_exercises = fields.List(fields.Nested(
        lambda: WorkoutExerciseSchema(exclude=("exercise",))
    ))

    workouts = fields.List(fields.Nested(
        lambda: WorkoutSchema(exclude=("exercises", "workout_exercises",))
    ))

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship('WorkoutExercises', back_populates='workout')

    exercises = db.relationship("Exercise", secondary="workout_exercises", back_populates='workouts')

    __table_args__ = (db.CheckConstraint('duration_minutes > 0', name='check_duration_positive'),)

    def __repr__(self):
        return f"<Workout(id={self.id}, date={self.date}, duration={self.duration_minutes}, notes={self.notes}m)>"

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Duration must be a positive integer.")
        return value

class WorkoutSchema(Schema):
    id = fields.Integer()
    date = fields.Date()
    duration_minutes = fields.Integer()
    notes = fields.String()

    workout_exercises = fields.List(fields.Nested(
        lambda: WorkoutExerciseSchema(exclude=("workout",))
    ))


class WorkoutExercises(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates="workout_exercises")
    exercise = db.relationship('Exercise', back_populates="workout_exercises")

    __table_args__ = (
        db.CheckConstraint('sets > 0', name='check_sets_positive'),
        db.CheckConstraint('reps >= 0', name='check_reps_non_negative'),
    )


class WorkoutExerciseSchema(Schema):
    id = fields.Integer()
    reps = fields.Integer()
    sets = fields.Integer()
    duration_seconds = fields.Integer()

    exercise = fields.Nested(lambda: ExerciseSchema(exclude=("workout_exercises", "workouts",)))
    workout = fields.Nested(lambda: WorkoutSchema(exclude=("workout_exercises",)))