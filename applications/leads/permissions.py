from rest_framework import permissions

from applications.account.choices import ORGANIZER, AGENT


class IsOrganizer(permissions.BasePermission):
    """
    The request user is an organizer user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(request.user.role == ORGANIZER and request.user.is_authenticated)


class IsOrganizerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.role == ORGANIZER
            and request.user.is_authenticated
        )


class IsAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == AGENT and request.user.is_authenticated)
