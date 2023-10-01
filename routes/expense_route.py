from flask import Blueprint, request, jsonify
import db.expense_db as expense_db
from models.expense import Expense, Participant
import logging

logger = logging.getLogger(__name__)
expense_routes = Blueprint('expense_routes', __name__)

@expense_routes.route('/expenses', methods=['POST'])
def create_expense():
    try:
        data = request.json
        participants = [Participant(user_id=participant['userId'], owed_amount=participant.get('owedAmount'), owed_percentage=participant.get('owedPercentage'))
                        for participant in data['participants']]
        expense = Expense(expense_id=data['expenseId'], payer_id=data['payerId'], amount=data['amount'], split_type=data['splitType'], participants=participants,
                          created_at=data['createdAt'], expense_name=data.get('expenseName'), notes=data.get('notes'), images=data.get('images'))
        expense_db.insert_expense(expense)
        return jsonify(expense.to_json()), 201
    except KeyError as e:
        logger.error(f"Missing required field: {e}")
        return jsonify({"error": "Bad Request", "message": f"Missing required field: {e}"}), 400
    except Exception as e:
        logger.error(f"Error creating expense: {e}")
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500

@expense_routes.route('/expenses/<expense_id>', methods=['GET'])
def get_expense(expense_id):
    try:
        expense = expense_db.get_expense(expense_id)
        if expense:
            return jsonify(expense.to_json())
        else:
            return jsonify({"error": "Expense not found"}), 404
    except Exception as e:
        logger.error(f"Error getting expense: {e}")
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500

@expense_routes.route('/expenses/<expense_id>', methods=['PUT'])
def update_expense(expense_id):
    try:
        data = request.json
        participants = [Participant(user_id=participant['userId'], owed_amount=participant.get('owedAmount'), owed_percentage=participant.get('owedPercentage'))
                        for participant in data['participants']]
        updated_expense = Expense(expense_id=expense_id, payer_id=data['payerId'], amount=data['amount'], split_type=data['splitType'], participants=participants,
                                  created_at=data['createdAt'], expense_name=data.get('expenseName'), notes=data.get('notes'), images=data.get('images'))
        expense_db.update_expense(expense_id, updated_expense)
        return jsonify(updated_expense.to_json())
    except KeyError as e:
        logger.error(f"Missing required field: {e}")
        return jsonify({"error": "Bad Request", "message": f"Missing required field: {e}"}), 400
    except Exception as e:
        logger.error(f"Error updating expense: {e}")
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500

@expense_routes.route('/expenses/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    try:
        expense_db.delete_expense(expense_id)
        return jsonify({"message": "Expense deleted"}), 200
    except Exception as e:
        logger.error(f"Error deleting expense: {e}")
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500
