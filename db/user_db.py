import logging
from pymongo import MongoClient
from models.user import User

logger = logging.getLogger(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['expense_sharing_app']
users_collection = db['users']

def insert_user(user):
    try:
        user_json = user.to_json()
        users_collection.insert_one(user_json)
        logger.info(f"Inserted user: {user.user_id}")
    except Exception as e:
        logger.error(f"Error inserting user: {e}")

def get_user(user_id):
    try:
        user_data = users_collection.find_one({"userId": user_id})
        if user_data:
            return User(
                user_id=user_data['userId'],
                name=user_data['name'],
                email=user_data['email'],
                mobile_number=user_data['mobileNumber'],
                is_active=user_data['isActive']
            )
    except Exception as e:
        logger.error(f"Error getting user: {e}")

def update_user(user_id, updated_user):
    try:
        users_collection.update_one({"userId": user_id}, {"$set": updated_user.to_json()})
        logger.info(f"Updated user: {user_id}")
    except Exception as e:
        logger.error(f"Error updating user: {e}")

def mark_user_inactive(user_id):
    try:
        users_collection.update_one({"userId": user_id}, {"$set": {"isActive": False}})
        logger.info(f"Marked user as inactive: {user_id}")
    except Exception as e:
        logger.error(f"Error marking user as inactive: {e}")
