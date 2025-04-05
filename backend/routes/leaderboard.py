from flask import Blueprint, request, jsonify
import uuid
from firebase_admin import db

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
        invite_link = str(uuid.uuid4())
        new_leaderboard_ref.update({'invite_link': invite_link})

        return jsonify({'message': 'Leaderboard created successfully', 'leaderboard_id': leaderboard_id, 'invite_link': invite_link}), 201
    except Exception as e:
        return jsonify({'message': f'Error creating leaderboard: {str(e)}'}), 500

@leaderboard_bp.route('/get/<leaderboard_id>', methods=['GET'])
def get_leaderboard(leaderboard_id):
    try:
        # Get the leaderboard from the database
        leaderboard_ref = db.reference(f'/leaderboards/{leaderboard_id}')
        leaderboard = leaderboard_ref.get()

        if not leaderboard:
            return jsonify({'message': 'Leaderboard not found'}), 404

        # Get the users from the leaderboard
        users = leaderboard.get('users', [])
        users_with_points = []
        for user_id in users:
            user_ref = db.reference(f'/users/{user_id}')
            user_data = user_ref.get()
            if user_data:
                users_with_points.append({
                    'user_id': user_id,
                    'username': user_data.get('username', ''),
                    'points': user_data.get('points', 0)
                })

        # Sort the users by points
        users_with_points.sort(key=lambda x: x['points'], reverse=True)

        return jsonify({'message': 'Leaderboard retrieved successfully', 'leaderboard': {
            'name': leaderboard.get('name', ''),
            'reset_date': leaderboard.get('reset_date', ''),
            'users': users_with_points
        }}), 200
    except Exception as e:
        return jsonify({'message': f'Error getting leaderboard: {str(e)}'}), 500

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

        # Sort the leaderboard
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

@leaderboard_bp.route('/invite/<invite_link>', methods=['POST'])
def join_leaderboard_with_invite(invite_link):
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({'message': 'Username is required'}), 400

    try:
        # Get the leaderboard from the database using the invite link
        leaderboard_ref = db.reference('/leaderboards')
        leaderboards = leaderboard_ref.get()

        leaderboard_id = None
        for key, value in leaderboards.items():
            if value.get('invite_link') == invite_link:
                leaderboard_id = key
                break

        if not leaderboard_id:
            return jsonify({'message': 'Invalid invite link'}), 404

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