from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

# Define Models here
class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Exercise(id={self.id}, name={self.name}, category={self.category}, equipment_needed={self.equipment_needed}m)>"

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.String)

    def __repr__(self):
        return f"<Workout(id={self.id}, date={self.date}, duration={self.duration_minutes}, notes={self.notes}m)>"