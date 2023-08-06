from revcore_micro.flask.exceptions import PermissionDenied

class BasePermission:
    def __init__(self, user):
        self.user = user

    def check_user_permission(self):
        raise NotImplementedError('check_user_permission')


class IsUserInValidGroups(BasePermission):
    valid_groups = []

    def check_user_permission(self):
        if not any([getattr(self.user, f'is_{group}') for group in self.valid_groups]):
            invalid_groups = ','.join(self.user.groups)
            valid_groups = ','.join(self.valid_groups)
            raise PermissionDenied(detail=f'invalid groups: {invalid_groups}; valid groups: {valid_groups}')
