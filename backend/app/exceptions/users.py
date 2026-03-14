from .auth import AccessDenied


class NoAllowedAddInOtherBranch(AccessDenied):
    _DETAILS = "Вы не можете добавлять пользователей в другой филиал"
