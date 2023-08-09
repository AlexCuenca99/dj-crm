from rest_framework import permissions

from applications.account.choices import ORGANIZER, AGENT


class IsOrganizer(permissions.BasePermission):
    """
    The request user is an organizer user, or is a read-only request.
    """

    message = {"errors": "Retrieve leads not allowed"}

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == ORGANIZER
            and request.user.is_authenticated
        )


class IsOrganizerOrReadOnly(permissions.BasePermission):
    message = {
        "errors": "User is not an organizer. You can just access to read only operations"
    }

    def has_permission(self, request, view) -> bool:
        return bool(
            (
                request.method in permissions.SAFE_METHODS
                and (request.user and request.user.is_authenticated)
            )
            and request.user.role == ORGANIZER
        )


class IsAgent(permissions.BasePermission):
    message = {
        "errors": "User is not an organizer. You can just access to read only operations"
    }

    def has_permission(self, request, view) -> bool:
        return bool(request.user.role == AGENT and request.user.is_authenticated)
