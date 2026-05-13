fake_users = [
    {"id": 1, "name": "Zeeshan", "email": "test@example.com"},
    {"id": 2, "name": "Ali", "email": "ali@example.com"},
]

def get_all_users():
    return fake_users

def get_user_by_id(user_id: int):
    return next((u for u in fake_users if u["id"] == user_id), None)