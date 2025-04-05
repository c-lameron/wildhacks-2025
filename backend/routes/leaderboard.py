from flask import Blueprint, request, jsonify
from models.leaderboard import Leaderboard

leaderboard_bp = Blueprint('leaderboard', __name__, url_prefix='/leaderboard')

@leaderboard_bp.route('/create', methods=['POST'])
def create_leaderboard():
    data = request.get_json()
    name = data.get('name')
    reset_date = data.get('reset_date')

    if not name:
        return jsonify({'message': 'Leaderboard name is required'}), 400

    try:
        # Save leaderboard to database
        ref = db.reference('/leaderboards')
        new_leaderboard_ref = ref.push({
            'name': name,
            'reset_date': reset_date
        })
        leaderboard_id = new_leaderboard_ref.key

        return jsonify({'message': 'Leaderboard created successfully', 'leaderboard_id': leaderboard_id}), 201
    except Exception as e:
        return jsonify({'message': f'Error creating leaderboard: {str(e)}'}), 500

@leaderboard_bp.route('/get/<leaderboard_id>', methods=['GET'])
def get_leaderboard(leaderboard_id):
    # TODO: Implement leaderboard retrieval logic (e.g., fetch from database)

    return jsonify({'message': 'Leaderboard retrieved successfully'}), 200

@leaderboard_bp.route('/join/<leaderboard_id>/<username>', methods=['POST'])
def join_leaderboard(leaderboard_id, username):
    try:
        # Get the leaderboard from the database
        leaderboard_ref = db.reference(f'/leaderboards/{leaderboard_id}')
        leaderboard = leaderboard_ref.get()

        if not leaderboard:
            return jsonify({'message': 'Leaderboard not found'}), 404

        # Add the user to the leaderboard's users list
        users = leaderboard.get('users', [])
        if username not in users:
            users.append(username)
            leaderboard_ref.update({'users': users})

        return jsonify({'message': 'User added to leaderboard successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error adding user to leaderboard: {str(e)}'}), 500

@leaderboard_bp.route('/reset/<leaderboard_id>', methods=['POST'])
def reset_leaderboard(leaderboard_id):
    try:
        # Get the leaderboard from the database
        leaderboard_ref = db.reference(f'/leaderboards/{leaderboard_id}')
        leaderboard = leaderboard_ref.get()

        if not leaderboard:
            return jsonify({'message': 'Leaderboard not found'}), 404

        # Reset the users list
        leaderboard_ref.update({'users': []})

        return jsonify({'message': 'Leaderboard reset successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error resetting leaderboard: {str(e)}'}), 500