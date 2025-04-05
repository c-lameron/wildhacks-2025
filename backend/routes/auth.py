from flask import Blueprint, request, jsonify
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # TODO: Implement user registration logic (e.g., check if user exists, hash password, save to database)

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # TODO: Implement user login logic (e.g., check if user exists, verify password)

    return jsonify({'message': 'User logged in successfully'}), 200