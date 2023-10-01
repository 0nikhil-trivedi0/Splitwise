class Participant:
    def __init__(self, user_id, owed_amount=0, owed_percentage=0):
        self.user_id = user_id
        self.owed_amount = owed_amount
        self.owed_percentage = owed_percentage
    
    def to_json(self):
        return {
            "userId": self.user_id,
            "owedAmount": self.owed_amount,
            "owedPercentage": self.owed_percentage
        }

class Expense:
    def __init__(self, expense_id, payer_id, amount, split_type, participants, created_at, expense_name=None, notes=None, images=None, needs_adjustment=False):
        self.expense_id = expense_id
        self.payer_id = payer_id
        self.amount = amount
        self.split_type = split_type
        self.participants = participants
        self.created_at = created_at
        self.expense_name = expense_name
        self.notes = notes
        self.images = images
        self.needs_adjustment = needs_adjustment
    
    def to_json(self):
        return {
            "expenseId": self.expense_id,
            "payerId": self.payer_id,
            "amount": self.amount,
            "splitType": self.split_type,
            "participants": [participant.to_json() for participant in self.participants],
            "createdAt": self.created_at,
            "expenseName": self.expense_name,
            "notes": self.notes,
            "images": self.images,
            "needsAdjustment": self.needs_adjustment
        }

def add_expense(expenses_list, expense):
    expenses_list.append(expense)

def split_expense(expense, users_list):
    num_participants = len(expense.participants)
    
    if expense.split_type == "EQUAL":
        owed_amount = expense.amount / num_participants
        for participant in expense.participants:
            participant.owed_amount = owed_amount
    
    elif expense.split_type == "EXACT":
        if not all(hasattr(participant, 'owed_amount') and participant.owed_amount is not None for participant in expense.participants):
            return "For EXACT split type, owed_amount must be set for each participant."
    
    elif expense.split_type == "PERCENT":
        for participant in expense.participants:
            participant.owed_amount = (expense.amount * participant.owed_percentage) / 100
    
    for participant in expense.participants:
        is_active = any(user.user_id == participant.user_id and user.is_active for user in users_list)
        if not is_active:
            expense.needs_adjustment = True
    
    return "Expense split successfully."
