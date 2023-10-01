import logging
from pymongo import MongoClient
from models.expense import Expense, Participant

logger = logging.getLogger(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['expense_sharing_app']
expenses_collection = db['expenses']

def insert_expense(expense):
    try:
        expense_json = expense.to_json()
        expenses_collection.insert_one(expense_json)
        logger.info(f"Inserted expense: {expense.expense_id}")
    except Exception as e:
        logger.error(f"Error inserting expense: {e}")

def get_expense(expense_id):
    try:
        expense_data = expenses_collection.find_one({"expenseId": expense_id})
        if expense_data:
            participants = [Participant(user_id=participant['userId'], owed_amount=participant['owedAmount'], owed_percentage=participant['owedPercentage'])
                            for participant in expense_data['participants']]
            return Expense(
                expense_id=expense_data['expenseId'],
                payer_id=expense_data['payerId'],
                amount=expense_data['amount'],
                split_type=expense_data['splitType'],
                participants=participants,
                created_at=expense_data['createdAt'],
                expense_name=expense_data.get('expenseName'),
                notes=expense_data.get('notes'),
                images=expense_data.get('images'),
                needs_adjustment=expense_data['needsAdjustment']
            )
    except Exception as e:
        logger.error(f"Error getting expense: {e}")

def update_expense(expense_id, updated_expense):
    try:
        expenses_collection.update_one({"expenseId": expense_id}, {"$set": updated_expense.to_json()})
        logger.info(f"Updated expense: {expense_id}")
    except Exception as e:
        logger.error(f"Error updating expense: {e}")

def delete_expense(expense_id):
    try:
        expenses_collection.delete_one({"expenseId": expense_id})
        logger.info(f"Deleted expense: {expense_id}")
    except Exception as e:
        logger.error(f"Error deleting expense: {e}")
