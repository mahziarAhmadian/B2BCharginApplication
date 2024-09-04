class CustomPermissions:
    def has_permission(self, request, view):
        # Define the required permission for the view
        required_permission = getattr(view, "required_permission", None)

        if required_permission:
            # Check if the user has the required permission
            return (
                request.user.is_superuser
                and required_permission in request.user.permissions
            )
        return True
