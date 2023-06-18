from database.models.db_user import DbUser


class DbUserHandler:
    def __init__(self):
        self._user: list[DbUser] = []
        self._user.append(DbUser("admin", "PmMukZoJZmxHgGLQpFgrM6KpPpM95QfXDNgf"))

    def get_user_by_username(self, username: str) -> DbUser:
        return next((user for user in self._user if user.username == username), None)
