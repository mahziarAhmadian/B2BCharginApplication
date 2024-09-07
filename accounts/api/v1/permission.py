from rest_framework.permissions import BasePermission


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_seller

    def has_object_permission(self, request, view, obj):
        if request.user.is_seller:
            return request.user.is_seller
