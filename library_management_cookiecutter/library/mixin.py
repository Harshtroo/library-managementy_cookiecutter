from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect


class MyCustomPermissions(PermissionRequiredMixin):
    def has_permission(self):
        user_permissions = self.request.user.get_all_permissions()
        if self.request.method == "GET":
            if self.permission_required.get("GET")[0] in user_permissions:
                return True
            return False

        if self.request.method == "POST":
            if self.permission_required.get("GET")[0] in user_permissions:
                return True
            return False

        permissions_required = [
            True if i in user_permissions else False for i in self.permission_required
        ]
        if self.request.user.is_authenticated and all(permissions_required):
            return True
        return False
