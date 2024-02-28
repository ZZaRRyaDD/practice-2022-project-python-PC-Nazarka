from rest_framework import permissions


class TargetPermissions(permissions.BasePermission):
    """Permission class for `Target` model."""

    def has_object_permission(self, request, view, obj) -> bool:
        """Method for check permissions of object."""
        if request.method in ('PUT', 'PATCH', 'DELETE'):
            return request.user == obj.user
        return True
