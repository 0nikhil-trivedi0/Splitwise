from flask import Blueprint, request, jsonify
import db.user_db as user_db
from models.user import User
import logging

logger = logging.getLogger(__name__)
user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        user = User(user_id=data['userId'], name=data['name'], email=data['email'], mobile_number=data['mobileNumber'])
        user_db.insert_user(user)
        return jsonify(user.to_json()), 201
    except KeyError as e:
        logger.error(f"Missing required field: {e}")
        return jsonify({"error": "Bad Request", "message": f"Missing required field: {e}"}), 400
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500

@user_routes.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = user_db.get_user(user_id)
        if user:
            return jsonify(user.to_json())
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500

@user_routes.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.json
        updated_user = User(user_id=user_id, name=data['name'], email=data['email'], mobile_number=data['mobileNumber'])
        user_db.update_user(user_id, updated_user)
        return jsonify(updated_user.to_json())
    except KeyError as e:
        logger.error(f"Missing required field: {e}")
        return jsonify({"error": "Bad Request", "message": f"Missing required field: {e}"}), 400
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500

@user_routes.route('/users/<user_id>', methods=['DELETE'])
def mark_user_inactive(user_id):
    try:
        user_db.mark_user_inactive(user_id)
        return jsonify({"message": "User marked as inactive"}), 200
    except Exception as e:
        logger.error(f"Error marking user as inactive: {e}")
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500
