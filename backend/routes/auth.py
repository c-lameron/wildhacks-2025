from flask import Blueprint, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Initialize Firebase Admin SDK with your credentials
# cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)


@auth_bp.route('/verify_token', methods=['POST'])
def verify_token():
    data = request.get_json()
    id_token = data.get('id_token')

    if not id_token:
        return jsonify({'message': 'ID token is required'}), 400

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return jsonify({'message': 'ID token is valid', 'uid': uid}), 200
    except Exception as e:
        return jsonify({'message': f'Invalid ID token: {str(e)}'}), 401

@auth_bp.route('/update_username', methods=['POST'])
def update_username():
    data = request.get_json()
    id_token = data.get('id_token')
    username = data.get('username')

    if not id_token:
        return jsonify({'message': 'ID token is required'}), 400

    if not username:
        return jsonify({'message': 'Username is required'}), 400

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Update the username in the Firebase database
        user = auth.update_user(uid, display_name=username)

        return jsonify({'message': 'Username updated successfully', 'uid': uid, 'username': username}), 200
    except Exception as e:
        return jsonify({'message': f'Error updating username: {str(e)}'}), 401