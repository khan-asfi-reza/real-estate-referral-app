from rest_framework.permissions import BasePermission


class RecruiterOnlyPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 1
