from flask import Flask
from routes.auth import auth_bp
from routes.task import task_bp
from routes.leaderboard import leaderboard_bp
import firebase_admin
from firebase_admin import credentials, db
import threading
import time
from datetime import datetime

app = Flask(__name__)

# Configure Gemini AI
gemini_api_key = "AIzaSyBLg8lFO_TW4MWuXoKAJihcQVFxSYgZbQQ"  # Replace with your actual API key
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-pro')

app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)
app.register_blueprint(leaderboard_bp)

# Initialize Firebase Admin SDK with your credentials
cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def reset_leaderboards():
    while True:
        now = datetime.now()
        leaderboard_ref = db.reference('/leaderboards')
        leaderboards = leaderboard_ref.get()

        if leaderboards:
            for leaderboard_id, leaderboard in leaderboards.items():
                reset_date_str = leaderboard.get('reset_date')
                if reset_date_str:
                    try:
                        reset_date = datetime.strptime(reset_date_str, '%Y-%m-%d')
                        if now.year == reset_date.year and now.month == reset_date.month and now.day == reset_date.day:
                            # Reset the users list
                            leaderboard_ref = db.reference(f'/leaderboards/{leaderboard_id}')
                            leaderboard_ref.update({'users': []})
                            print(f"Leaderboard {leaderboard_id} reset successfully")
                    except ValueError:
                        print(f"Invalid reset date format for leaderboard {leaderboard_id}")

        # Check every day
        time.sleep(24 * 60 * 60)

# Start the background task
threading.Thread(target=reset_leaderboards, daemon=True).start()

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)