from flask import Flask, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()

@app.route('/workouts', methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(workouts_schema.dump(workouts), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    workout = Workout.query.filter_by(id=id).first()
    if not workout:
        return make_response({"error": "Workout not found"}, 404)
    serialized_workout = workout_schema.dump(workout)
    return make_response(serialized_workout, 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    json_data = request.get_json()
    try:
        data = workout_schema.load(json_data)
        new_workout = Workout(**data)
        db.session.add(new_workout)
        db.session.commit()

        return make_response(workout_schema.dump(new_workout), 201)
    except ValidationError as err:
        return make_response(err.messages, 400)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)
    db.session.delete(workout)
    db.session.commit()
    return make_response({}, 204)


@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(exercises_schema.dump(exercises), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)
    return make_response(exercise_schema.dump(exercise), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json())
        new_exercise = Exercise(**data)
        db.session.add(new_exercise)
        db.session.commit()
        return make_response(exercise_schema.dump(new_exercise), 201)
    except ValidationError as err:
        return make_response(err.messages, 400)


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
    json_data = request.get_json()
    json_data['workout_id'] = workout_id
    json_data['exercise_id'] = exercise_id
    try:
        data = workout_exercise_schema.load(json_data)
        new_we = WorkoutExercises(**data)
        db.session.add(new_we)
        db.session.commit()
        return make_response(workout_exercise_schema.dump(new_we), 201)
    except ValidationError as err:
        return make_response(err.messages, 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)