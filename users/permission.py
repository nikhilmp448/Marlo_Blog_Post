from rest_framework import permissions

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff == False:
            return request.user 