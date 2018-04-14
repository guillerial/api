from rest_framework.permissions import BasePermission

from .models import Student, Teacher, Admin


class IsStudent(BasePermission):
    """
    Allows access only to student users.
    """

    def has_permission(self, request, view):
        try:
            Student.objects.get(email=request.user.username)
            return True
        except Student.DoesNotExist:
            return False



class IsTeacher(BasePermission):
    """
    Allows access only to teacher users.
    """
    def has_permission(self, request, view):
        try:
            Teacher.objects.get(email=request.user.username)
            return True
        except Teacher.DoesNotExist:
            return False


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        try:
            Admin.objects.get(email=request.user.username)
            return True
        except Admin.DoesNotExist:
            return False


def permission_class(profile_list):

    class Permission(BasePermission):

        def has_permission(self, request, view):
            for profile in profile_list:
                if profile.objects.filter(email=request.user.username).count() > 0:
                    return True

            return False
    return Permission
