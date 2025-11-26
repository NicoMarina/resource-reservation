class RoleChecker:
    """Encapsulates the logic of user roles"""

    def __init__(self, user):
        self.user = user

    def is_manager(self) -> bool:
        return self.user.groups.filter(name="manager").exists()

    def is_worker(self) -> bool:
        return self.user.groups.filter(name="worker").exists()


class ReservationStatusResolver:
    """Determines the reservation status according to the user's role"""

    def __init__(self, role_checker: RoleChecker):
        self.role_checker = role_checker

    def get_status(self):
        if self.role_checker.is_manager():
            return "approved", self.role_checker.user
        return "pending", None
