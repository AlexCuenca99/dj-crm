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
        if not request.user.is_authenticated:
            return False

        if view.action == "retrieve" or view.action == "list":
            return True
        elif (
            view.action == "create"
            or view.action == "update"
            or view.action == "partial_update"
            or view.action == "destroy"
        ):
            return request.user.role == ORGANIZER


class IsAgent(permissions.BasePermission):
    message = {
        "errors": "User is not an organizer. You can just access to read only operations"
    }

    def has_permission(self, request, view) -> bool:
        return bool(request.user.role == AGENT and request.user.is_authenticated)
