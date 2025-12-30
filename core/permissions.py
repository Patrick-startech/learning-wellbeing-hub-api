from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Allow access only to Admin users."""
    def has_permission(self, request, _):
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", None) == "admin"
        )


class IsMentorAdminOrReadOnly(BasePermission):
    """
    SAFE METHODS (GET, HEAD, OPTIONS):
        - Everyone can view quizzes and questions.
    
    UNSAFE METHODS (POST, PUT, PATCH, DELETE):
        - Only mentors or admins can modify quiz content.
    """
    def has_permission(self, request, _):
        if request.method in SAFE_METHODS:
            return True

        user_role = getattr(request.user, 'role', None)
        return user_role in ['mentor', 'admin']


class IsStudent(BasePermission):
    """Allow access only to Students."""
    def has_permission(self, request, _):
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", None) == "student"
        )


class ReadOnly(BasePermission):
    """Allow read-only requests for any authenticated user."""
    def has_permission(self, request, _):
        return request.user.is_authenticated and request.method in SAFE_METHODS


# -------------------------
# Extra Permissions for Hub
# -------------------------

class IsOwnerOrAdmin(BasePermission):
    """
    Allow access if the user owns the object or is an Admin.
    """
    def has_object_permission(self, request, _, obj):
        return (
            request.user.is_authenticated
            and (obj.user == request.user or getattr(request.user, "role", None) == "admin")
        )


class IsMentor(BasePermission):
    """Allow access only to Mentors."""
    def has_permission(self, request, _):
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", None) == "mentor"
        )


class IsForumModeratorOrAdmin(BasePermission):
    """
    Allow forum moderation actions for Admins or Mentors.
    """
    def has_permission(self, request, _):
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", None) in ["admin", "mentor"]
        )
