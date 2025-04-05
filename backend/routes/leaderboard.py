from flask import Blueprint, request, jsonify
from models.leaderboard import Leaderboard

leaderboard_bp = Blueprint('leaderboard', __name__, url_prefix='/leaderboard')

@leaderboard_bp.route('/create', methods=['POST'])
def create_leaderboard():
    data = request.get_json()
    name = data.get('name')
    reset_date = data.get('reset_date')

    # TODO: Implement leaderboard creation logic (e.g., save to database)

    return jsonify({'message': 'Leaderboard created successfully'}), 201

@leaderboard_bp.route('/get/<leaderboard_id>', methods=['GET'])
def get_leaderboard(leaderboard_id):
    # TODO: Implement leaderboard retrieval logic (e.g., fetch from database)

    return jsonify({'message': 'Leaderboard retrieved successfully'}), 200

@leaderboard_bp.route('/join/<leaderboard_id>/<username>', methods=['POST'])
def join_leaderboard(leaderboard_id, username):
    # Implement logic to add user to leaderboard (e.g., update database)
    # Assuming you have a Leaderboard object and a method to add users
    # Retrieve the leaderboard from the database using the leaderboard_id
    # leaderboard = Leaderboard.get(leaderboard_id)
    # if leaderboard:
    #     leaderboard.add_user(username)
    #     # Save the updated leaderboard to the database
    #     # leaderboard.save()
    #     return jsonify({'message': 'User added to leaderboard successfully'}), 200
    # else:
    #     return jsonify({'message': 'Leaderboard not found'}), 404
    return jsonify({'message': 'User added to leaderboard successfully'}), 200