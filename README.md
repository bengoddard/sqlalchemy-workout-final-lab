# sqlalchemy-workout-final-lab

This is a project that helps you keep track of your workouts and the exercises in each workout.

Run 'pipenv install' and 'pipenv shell'
Cd to server 'cd server'
Then run 'flask db init', 'flask db migrate -m 'initial migration'', and 'flask db upgrade head'.
Then run 'python seed.py' to seed the database.
Run 'export FLASK_APP=app.py'
Run 'export FLASK_RUN_PORT=5555'
Then run 'flask run' to start the server.


Here are all endpoints for the API:
/workouts
/workouts/<id>
/exercises
/exercises/<id>
