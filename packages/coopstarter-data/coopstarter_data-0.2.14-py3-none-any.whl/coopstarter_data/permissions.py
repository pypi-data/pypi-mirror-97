from djangoldp.permissions import LDPPermissions


class PendingResourcePermissions(LDPPermissions):
    anonymous_perms = []
    authenticated_perms = ['view', 'add', 'delete', 'change']

    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True

        if request.user.is_anonymous:
            return False
        return True
