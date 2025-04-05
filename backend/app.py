from flask import Flask
from routes.auth import auth_bp
from routes.task import task_bp
from routes.leaderboard import leaderboard_bp  # Import the leaderboard blueprint

app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)
app.register_blueprint(leaderboard_bp)  # Register the leaderboard blueprint

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)