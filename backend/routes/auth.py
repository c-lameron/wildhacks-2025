from flask import Blueprint, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# TODO: Initialize Firebase Admin SDK with your credentials
# cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return jsonify({'message': 'User registered successfully', 'uid': user.uid}), 201
    except Exception as e:
        return jsonify({'message': f'Error registering user: {str(e)}'}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try:
        user = auth.get_user_by_email(email)
        # TODO: Implement password verification (Firebase doesn't directly support password verification)
        # You might need to store a hash of the password in Firebase and verify it here

        return jsonify({'message': 'User logged in successfully', 'uid': user.uid}), 200
    except Exception as e:
        return jsonify({'message': f'Error logging in: {str(e)}'}), 401