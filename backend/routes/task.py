from flask import Blueprint, request, jsonify
import firebase_admin
from backend.app import model
from firebase_admin import credentials, auth, db
from models.task import Task

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
    # TODO: Implement task completion logic (e.g., update task status, award points to user)

    return jsonify({'message': 'Task completed successfully'}), 200