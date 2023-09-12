from .permissions import IsStaffPermission
from rest_framework import permissions


class StaffMixinPermissions():
    permission_classes = [permissions.IsAdminUser, IsStaffPermission]
