from apps.users.models import User


class IsAdmin:
    @staticmethod
    def is_admin(user: User) -> bool:
        return user.role == "admin"
