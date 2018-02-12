from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Student
from .serializers import RegisterSerializer

# Create your views here.


class IndexView(APIView):

    def get(self, request):

        urls = {
            'Register': reverse('register', request=request),
        }

        return Response(urls)


index = IndexView.as_view()


class RegisterView(APIView):
    """
    Creates the user.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(email=serializer.data['email'])
        except Student.DoesNotExist:
            student = Student.create_new_student(name=serializer.data['name'],
                                                 email=serializer.data['email'],
                                                 password=serializer.data['password'])
            student.save()

        django_user, created = User.objects.get_or_create(username=serializer.data['email'])

        if django_user is None or not django_user.is_active:
            return Response(data={"detail: User don't exist"},
                            status=status.HTTP_403_FORBIDDEN)

        token, create = Token.objects.get_or_create(user=django_user)
        json = serializer.data
        json['token'] = token.key
        return Response(json, status=status.HTTP_201_CREATED)


user_register = RegisterView.as_view()
