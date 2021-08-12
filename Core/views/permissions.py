from rest_framework.permissions import BasePermission


class RecruiterOnlyPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 1


class RecruitOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 2
