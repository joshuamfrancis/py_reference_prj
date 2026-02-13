"""API routes"""
from flask import Blueprint, request, jsonify
from app.models import user_store

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


@api_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = user_store.get_all_users()
    return jsonify([user.to_dict() for user in users]), 200


@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    user = user_store.get_user(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404


@api_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Missing required fields: name, email"}), 400

    user = user_store.create_user(name, email)
    return jsonify(user.to_dict()), 201


@api_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user information"""
    user = user_store.get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get('name')
    email = data.get('email')

    updated_user = user_store.update_user(user_id, name, email)
    return jsonify(updated_user.to_dict()), 200


@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user by ID"""
    if user_store.delete_user(user_id):
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404


@api_bp.route('/users/count', methods=['GET'])
def count_users():
    """Get total user count"""
    count = len(user_store.get_all_users())
    return jsonify({"total_users": count}), 200
