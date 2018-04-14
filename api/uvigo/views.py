from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Student, Group, Topology, Indications, Classroom, Teacher, Schedule
from . import serializers, permissions

# Create your views here.


class IndexView(APIView):

    def get(self, request):

        urls = {
            'Register': reverse('register', request=request),
            'Login': reverse('login', request=request),
        }

        return Response(urls)


index = IndexView.as_view()


class RegisterView(APIView):
    """
    Creates the user.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(email=serializer.data['email'])
            return Response(data={"detail": "User already exist"},
                            status=status.HTTP_403_FORBIDDEN)
        except Student.DoesNotExist:
            try:
                student = Student.objects.get(name=serializer.data['name'])
                student.assign_email_and_password(email=serializer.data['email'],
                                                     password=serializer.data['password'])
                student.save()
                print("asd")
            except Student.DoesNotExist:
                student = Student.create_new_student(name=serializer.data['name'],
                                                     email=serializer.data['email'],
                                                     password=serializer.data['password'])
                student.save()
                print("asdf")

        django_user, created = User.objects.get_or_create(username=serializer.data['email'])

        if django_user is None or not django_user.is_active:
            return Response(data={"detail": "User don't exist"},
                            status=status.HTTP_403_FORBIDDEN)

        token, create = Token.objects.get_or_create(user=django_user)
        json = dict(serializer.data)
        json['token'] = token.key
        del json['password']
        return Response(json, status=status.HTTP_201_CREATED)


user_register = RegisterView.as_view()


class LoginView(APIView):
    """
    Return user's token.
    """
    permission_classes = (AllowAny,)

    def post(self, request):

        serializer = serializers.LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Student.objects.get(email=serializer.data['email'])
            if user.check_password(serializer.data['password']):
                django_user = User.objects.get(username=serializer.data['email'])
                token, create = Token.objects.get_or_create(user=django_user)
                return Response(data={"token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response(data={"detail": "wrong password"}, status=status.HTTP_403_FORBIDDEN)

        except Student.DoesNotExist:
            return Response(data={"detail": "User don't exist"},
                            status=status.HTTP_403_FORBIDDEN)


user_login = LoginView.as_view()


class ProfileView(APIView):
    """
    Return user's profile data.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = Student.objects.get(email=request.user.username)
            return Response(data=serializers.ProfileSerializer(instance=user).data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response(data={"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


user_profile = ProfileView.as_view()


class TopologyView(APIView):
    """
    Returns topology info
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        objs = Topology.objects.all()

        return Response(data=serializers.TopologySerializer(instance=objs, many=True).data, status=status.HTTP_200_OK)


topology_data = TopologyView.as_view()


class IndicationsView(APIView):
    """
    Returns indications
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        objs = Indications.objects.all()

        return  Response(data=serializers.IndicationSerializer(instance=objs, many=True).data, status=status.HTTP_200_OK)


indications_data = IndicationsView.as_view()


class ClassroomsView(APIView):
    """
    Returns classrooms
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        objs = Classroom.objects.all()

        return  Response(data=serializers.FullClassroomSerializer(instance=objs, many=True).data, status=status.HTTP_200_OK)


classrooms = ClassroomsView.as_view()


class TeachersView(APIView):
    """
    Returns teachers
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        objs = Teacher.objects.all()

        return Response(data=serializers.TeacherSerializer(instance=objs, many=True).data, status=status.HTTP_200_OK)


teachers = TeachersView.as_view()


class SchedulesView(APIView):
    """
    Returns schedules
    """
    permission_classes = (IsAuthenticated, permissions.IsStudent)

    def get(self, request):
        user = Student.objects.get(email=request.user.username)

        objs = Schedule.objects.filter(group__students__id=user.id)

        return Response(data=serializers.ScheduleSerializer(instance=objs, many=True).data, status=status.HTTP_200_OK)


schedules = SchedulesView.as_view()