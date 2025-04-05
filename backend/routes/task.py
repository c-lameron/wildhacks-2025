from flask import Blueprint, request, jsonify
from models.task import Task

task_bp = Blueprint('task', __name__, url_prefix='/task')

@task_bp.route('/add', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    # TODO: Integrate with Gemini AI to get difficulty rating
    difficulty = 5  # Placeholder difficulty

    # TODO: Save task to database

    return jsonify({'message': 'Task added successfully', 'difficulty': difficulty}), 201

@task_bp.route('/complete/<task_id>', methods=['POST'])
def complete_task(task_id):
    # TODO: Implement task completion logic (e.g., update task status, award points to user)

    return jsonify({'message': 'Task completed successfully'}), 200