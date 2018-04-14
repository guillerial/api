from .models import Student, Admin, Teacher, UvigoUser


class Utils:

    @staticmethod
    def check_user_and_type(email):
        if Admin.objects.filter(email=email).count() > 0:
            return Admin.objects.get(email=email), UvigoUser.ADMIN
        if Teacher.objects.filter(email=email).count() > 0:
            return Teacher.objects.get(email=email), UvigoUser.TEACHER
        if Student.objects.filter(email=email).count() > 0:
            return Student.objects.get(email=email), UvigoUser.STUDENT

