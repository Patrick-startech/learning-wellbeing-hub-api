from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Allow access only to Admin users."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", None) == "admin"
        )


class IsMentorOrAdmin(BasePermission):
    """Allow access to Mentors and Admins."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", None) in ["mentor", "admin"]
        )


class IsStudent(BasePermission):
    """Allow access only to Students."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", None) == "student"
        )


class ReadOnly(BasePermission):
    """Allow read-only requests for any authenticated user."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.method in SAFE_METHODS


# -------------------------
# Extra Permissions for Hub
# -------------------------

class IsOwnerOrAdmin(BasePermission):
    """
    Allow access if the user owns the object (e.g., journal entry, forum post)
    or is an Admin.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (obj.user == request.user or getattr(request.user, "role", None) == "admin")
        )


class IsMentor(BasePermission):
    """Allow access only to Mentors."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", None) == "mentor"
        )


class IsForumModeratorOrAdmin(BasePermission):
    """
    Allow forum moderation actions for Admins or Mentors (acting as moderators).
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", None) in ["admin", "mentor"]
        )
