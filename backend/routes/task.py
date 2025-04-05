from flask import Blueprint, request, jsonify
import firebase_admin
from backend.app import model
from firebase_admin import credentials, auth, db

task_bp = Blueprint('task', __name__, url_prefix='/task')

@task_bp.route('/add', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    # Integrate with Gemini AI to get difficulty rating
    prompt = f"Rate the difficulty of this task on a scale of 1 to 5: {description}"
    response = model.generate_content(prompt)
    difficulty = int(response.text)  # Difficulty must be a whole number

    # Save task to database
    ref = db.reference('/tasks')
    new_task_ref = ref.push({
        'title': title,
        'description': description,
        'difficulty': difficulty
    })
    task_id = new_task_ref.key

    return jsonify({'message': 'Task added successfully', 'difficulty': difficulty, 'task_id': task_id}), 201

@task_bp.route('/complete/<task_id>', methods=['POST'])
def complete_task(task_id):
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'message': 'User ID is required'}), 400

    try:
        # Get the task from the database
        task_ref = db.reference(f'/tasks/{task_id}')
        task = task_ref.get()

        if not task:
            return jsonify({'message': 'Task not found'}), 404

        difficulty = task.get('difficulty')

        # Update the user's points in the database
        user_ref = db.reference(f'/users/{user_id}')
        user = user_ref.get()

        if not user:
            return jsonify({'message': 'User not found'}), 404

        current_points = user.get('points', 0)
        new_points = current_points + difficulty

        user_ref.update({'points': new_points})

        # Sort the leaderboard
        leaderboard_ref = db.reference('/leaderboards')
        leaderboards = leaderboard_ref.get()

        if leaderboards:
            for leaderboard_id, leaderboard in leaderboards.items():
                if leaderboard and 'users' in leaderboard:
                    users = leaderboard.get('users', [])
                    # Sort the users by points
                    users_with_points = []
                    for user_id in users:
                        user_ref = db.reference(f'/users/{user_id}')
                        user_data = user_ref.get()
                        if user_data:
                            users_with_points.append((user_id, user_data.get('points', 0)))

                    users_with_points.sort(key=lambda x: x[1], reverse=True)
                    sorted_users = [user_id for user_id, points in users_with_points]
                    leaderboard_ref = db.reference(f'/leaderboards/{leaderboard_id}')
                    leaderboard_ref.update({'users': sorted_users})

        return jsonify({'message': 'Task completed successfully', 'points_awarded': difficulty, 'new_points': new_points}), 200
    except Exception as e:
        return jsonify({'message': f'Error completing task: {str(e)}'}), 500