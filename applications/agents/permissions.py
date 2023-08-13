from rest_framework import permissions

from applications.account.choices import AGENT


class IsAssignedOrReadOnly(permissions.BasePermission):
    message = {
        "errors": "You are not the assigned agent. You can just access to read only operations"
    }

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.agent.user == request.user
