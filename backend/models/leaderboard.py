class Leaderboard:
    def __init__(self, id, name, reset_date):
        self.id = id
        self.name = name
        self.reset_date = reset_date
        self.users = []

    def add_user(self, username):
        self.users.append(username)