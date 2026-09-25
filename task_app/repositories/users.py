users = {
    "username": {
        "username": "username",
        "email": "email@email.net",
        "password": "pass123"
    }
}

class UserRepository:
    def get_user_by_username(self, username):
        user = users.get(username, None)

        return user

    def create_user(self, username: str, email, password: str):
        users[username] = {
            "username": username,
            "email": email,
            "password": password
        }

    def get_all_users(self):
        return users


    def edit_user(self, username: str, upd_data: dict):
        users[username].update(**upd_data)

    def delete_user(self, username: str):
        users.pop(username)


