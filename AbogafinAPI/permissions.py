from rest_framework.permissions import BasePermission, IsAuthenticated


class AdminOrSelf(IsAuthenticated):

    def has_permission(self, request, view):
        if (request.user.is_staff):
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if (request.user.is_staff):
            return True
        elif (request.user == obj):
            return True
        return False
