class User:
    def __init__(self, user_id, name, email, mobile_number, is_active=True):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.mobile_number = mobile_number
        self.is_active = is_active
    
    def to_json(self):
        return {
            "userId": self.user_id,
            "name": self.name,
            "email": self.email,
            "mobileNumber": self.mobile_number,
            "isActive": self.is_active
        }
    
    def mark_inactive(self):
        self.is_active = False


def add_user(users_list, user):
    users_list.append(user)


def mark_user_inactive(users_list, user_id):
    for user in users_list:
        if user.user_id == user_id:
            user.mark_inactive()
