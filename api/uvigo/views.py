from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from pyfcm import FCMNotification
from pyfcm.errors import FCMError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Student, Group, Topology, Indications, Classroom, Teacher, Schedule, Admin, UvigoUser, TeacherSchedule
from . import serializers, permissions
from .utils import Utils
from api import settings

# Create your views here.


class IndexView(APIView):

    def get(self, request):

        urls = {
            'Register': reverse('register', request=request),
            'Login': reverse('login', request=request),
        }

        return Response(urls)


index = IndexView.as_view()


class StudentRegisterView(APIView):
    """
    Creates a student.
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
            except Student.DoesNotExist:
                student = Student.create_new_student(name=serializer.data['name'],
                                                     email=serializer.data['email'],
                                                     password=serializer.data['password'])
                student.save()

        django_user, created = User.objects.get_or_create(username=serializer.data['email'])

        if django_user is None or not django_user.is_active:
            return Response(data={"detail": "User don't exist"},
                            status=status.HTTP_403_FORBIDDEN)

        token, create = Token.objects.get_or_create(user=django_user)
        json = dict(serializer.data)
        json['token'] = token.key
        del json['password']
        return Response(json, status=status.HTTP_201_CREATED)


student_register = StudentRegisterView.as_view()


class TeacherRegisterView(APIView):
    """
    Creates a teacher.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            teacher = Teacher.objects.get(email=serializer.data['email'])
            return Response(data={"detail": "User already exist"},
                            status=status.HTTP_403_FORBIDDEN)
        except Teacher.DoesNotExist:
            try:
                teacher = Teacher.objects.get(name=serializer.data['name'])
                teacher.assign_email_and_password(email=serializer.data['email'],
                                                     password=serializer.data['password'])
                teacher.save()

            except Teacher.DoesNotExist:
                teacher = Teacher.create_new_teacher(name=serializer.data['name'],
                                                     email=serializer.data['email'],
                                                     password=serializer.data['password'])
                teacher.save()

        django_user, created = User.objects.get_or_create(username=serializer.data['email'])

        if django_user is None or not django_user.is_active:
            return Response(data={"detail": "User don't exist"},
                            status=status.HTTP_403_FORBIDDEN)

        token, create = Token.objects.get_or_create(user=django_user)
        json = dict(serializer.data)
        json['token'] = token.key
        del json['password']
        return Response(json, status=status.HTTP_201_CREATED)


teacher_register = TeacherRegisterView.as_view()


class AdminRegisterView(APIView):
    """
    Creates a teacher.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            admin = Admin.objects.get(email=serializer.data['email'])
            return Response(data={"detail": "User already exist"},
                            status=status.HTTP_403_FORBIDDEN)
        except Admin.DoesNotExist:
            try:
                admin = Admin.objects.get(name=serializer.data['name'])
                admin.assign_email_and_password(email=serializer.data['email'],
                                                     password=serializer.data['password'])
                admin.save()

            except Admin.DoesNotExist:
                admin = Admin.create_new_admin(name=serializer.data['name'],
                                                     email=serializer.data['email'],
                                                     password=serializer.data['password'])
                admin.save()

        django_user, created = User.objects.get_or_create(username=serializer.data['email'])

        if django_user is None or not django_user.is_active:
            return Response(data={"detail": "User don't exist"},
                            status=status.HTTP_403_FORBIDDEN)

        token, create = Token.objects.get_or_create(user=django_user)
        json = dict(serializer.data)
        json['token'] = token.key
        del json['password']
        return Response(json, status=status.HTTP_201_CREATED)


admin_register = AdminRegisterView.as_view()


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
                return Response(data={"token": token.key , "name": user.name, "user_type": "student"}, status=status.HTTP_200_OK)
            else:
                return Response(data={"detail": "wrong password"}, status=status.HTTP_403_FORBIDDEN)

        except Student.DoesNotExist:

            try:
                user = Teacher.objects.get(email=serializer.data['email'])
                if user.check_password(serializer.data['password']):
                    django_user = User.objects.get(username=serializer.data['email'])
                    token, create = Token.objects.get_or_create(user=django_user)
                    return Response(data={"token": token.key, "name": user.name, "user_type": "teacher"}, status=status.HTTP_200_OK)
                else:
                    return Response(data={"detail": "wrong password"}, status=status.HTTP_403_FORBIDDEN)

            except Teacher.DoesNotExist:

                try:
                    user = Admin.objects.get(email=serializer.data['email'])
                    if user.check_password(serializer.data['password']):
                        django_user = User.objects.get(username=serializer.data['email'])
                        token, create = Token.objects.get_or_create(user=django_user)
                        return Response(data={"token": token.key, "name": user.name, "user_type": "admin"}, status=status.HTTP_200_OK)
                    else:
                        return Response(data={"detail": "wrong password"}, status=status.HTTP_403_FORBIDDEN)

                except Admin.DoesNotExist:
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
            try:
                user = Teacher.objects.get(email=request.user.username)
                return Response(data=serializers.TeacherSerializer(instance=user).data, status=status.HTTP_200_OK)
            except Teacher.DoesNotExist:
                try:
                    user = Admin.objects.get(email=request.user.username)
                    return Response(data=serializers.UserSerializer(instance=user).data, status=status.HTTP_200_OK)
                except Admin.DoesNotExist:
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
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user, user_type = Utils.check_user_and_type(request.user.username)
        if user_type == UvigoUser.STUDENT:
            user = Student.objects.get(email=request.user.username)

            objs = Schedule.objects.filter(group__students__id=user.id)

            return Response(data=serializers.ScheduleSerializer(instance=objs, many=True).data, status=status.HTTP_200_OK)

        elif user_type == UvigoUser.TEACHER:
            user = Teacher.objects.get(email=request.user.username)

            objs = TeacherSchedule.objects.filter(teacher__id=user.id)

            return Response(data=serializers.TeacherScheduleSerializer(instance=objs, many=True).data,
                            status=status.HTTP_200_OK)
        else:
            return Response(data={"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


schedules = SchedulesView.as_view()


class UsersListView(APIView):
    """
    Returns schedules
    """
    permission_classes = (IsAuthenticated, permissions.IsAdmin)

    def get(self, request):

        class AuxObject:
            students = Student.objects.all()
            teachers = Teacher.objects.all()

        aux = AuxObject()

        return Response(data=serializers.UserByTypeSerializer(instance=aux).data, status=status.HTTP_200_OK)


users_list = UsersListView.as_view()


class GroupsView(APIView):
    """
    Returns user groups
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = serializers.GroupViewSerializer(data=request.GET)
        user, user_type = Utils.check_user_and_type(request.user.username)
        if serializer.is_valid(raise_exception=True):
            if user_type == UvigoUser.ADMIN:

                if 'id' in serializer.validated_data.keys():
                    if serializer.validated_data['type'] == UvigoUser.TEACHER:
                        return Response(serializers.GroupSerializer(instance=Group.objects.filter(teacher__id=serializer.validated_data['id']).data, many=True).data,
                                        status=status.HTTP_200_OK)
                    if serializer.validated_data['type'] == UvigoUser.STUDENT:
                        return Response(serializers.GroupSerializer(instance=Group.objects.filter(students__id=serializer.validated_data['id']).data, many=True).data,
                                        status=status.HTTP_200_OK)
                    return Response(data={"detail": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

                elif 'subject' in serializer.validated_data.keys():
                    groups = Group.objects.filter(subject_name=serializer.validated_data['subject'])
                    if groups:
                        return Response(
                            serializers.GroupSerializer(instance=groups,
                                                        many=True).data,
                            status=status.HTTP_200_OK)
                else:
                    return Response(data={"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

            elif user_type == UvigoUser.TEACHER:
                groups = Group.objects.filter(teacher__id=user.id)
                return Response(
                    serializers.GroupSerializer(instance=groups,
                                                many=True).data,
                    status=status.HTTP_200_OK)
            return Response(data={"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = serializers.ModifyGroupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            group = Group.objects.get(serializer.data['code'])
            serializer.update(group, serializer.validated_data)
            return Response(data={"detail": "OK"}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.ModifyGroupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response(data={"detail": "OK"}, status=status.HTTP_201_CREATED)


groups = GroupsView.as_view()


class FCMInstanceView(APIView):
    push_service = FCMNotification(api_key=settings.FIREBASE_API_KEY)

    permission_classes = (IsAuthenticated, permissions.IsStudent)

    def post(self, request):

        firebase_token = request.data['firebase_token']

        user, user_type = Utils.check_user_and_type(request.user.username)

        if user.firebase_token is not None:
            self.push_service.unsubscribe_registration_ids_from_topic([user.firebase_token, ], 'markn')

        user.firebase_token = firebase_token

        user.save()

        self.push_service.subscribe_registration_ids_to_topic([firebase_token, ], 'markn')

        return Response(data={"detail": "Firebase instance sent"}, status=status.HTTP_200_OK)


firebase_token = FCMInstanceView.as_view()


class FCMView(APIView):
    push_service = FCMNotification(api_key=settings.FIREBASE_API_KEY)
    serializer_class = serializers.FCMSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            message_title = None

            data_message = {'author': serializer.validated_data['author']}

            if "title" in serializer.validated_data.keys():
                message_title = serializer.validated_data['title']

            self.push_service.notify_topic_subscribers(topic_name="markn",
                                                       message_body=serializer.validated_data['body'],
                                                       message_title=message_title,
                                                       data_message=data_message)

            return Response(data={'detail': 'Notification sent'}, status=status.HTTP_200_OK)


firebase = FCMView.as_view()
