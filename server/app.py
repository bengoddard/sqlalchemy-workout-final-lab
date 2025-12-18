from flask import Flask, make_response, request
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/workouts', methods=["GET"])
def get_workouts():
    workouts = []
    for w in Workout.query.all():
        w_dict = {"id": w.id,
                  "date": w.date,
                  "duration_minutes": w.duration_minutes,
                  "notes": w.notes}
        workouts.append(w_dict)
    if not workouts:
        return make_response({"error": 'There are no workouts'}), 404
    return make_response(workouts), 200

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    workout = Workout.query.filter_by(id=id).first()
    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    return make_response(workout), 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()

    try:
        new_workout = Workout(
            date=data.get('date'),
            duration_minutes=data.get('duration_minutes'),
            notes=data.get('notes')
        )

        db.session.add(new_workout)
        db.session.commit()

        return make_response(new_workout), 201

    except ValueError as e:
        # This catches your @validates('duration_minutes') error
        return make_response({"errors": [str(e)]}, 400)
    except Exception as e:
        return make_response({"errors": ["Internal Server Error"]}, 500)

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.filter_by(id=id).first()
    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    db.session.delete(workout)
    db.session.commit()

    return make_response({}, 204)

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(exercises), 200

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    exercise = Exercise.query.filter_by(id=id).first()
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)
    return make_response(exercise), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    try:
        new_ex = Exercise(
            name=data.get('name'),
            category=data.get('category'),
            equipment_needed=data.get('equipment_needed')
        )
        db.session.add(new_ex)
        db.session.commit()
        return make_response(new_ex), 201
    except ValueError as e:
        return make_response({"errors": [str(e)]}, 400)

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.filter_by(id=id).first()
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)

    db.session.delete(exercise)
    db.session.commit()
    return make_response({}, 204)

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout or not exercise:
        return make_response({"error": "Workout or Exercise not found"}, 404)

    data = request.get_json()

    try:

        new_we = WorkoutExercises(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )

        db.session.add(new_we)
        db.session.commit()


        return make_response(workout), 201

    except ValueError as e:
        return make_response({"errors": [str(e)]}, 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)