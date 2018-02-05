from django.shortcuts import render

from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse

from legacy.models import Question, Choice
from api import settings


# Create your views here.

class IndexView(APIView):

    def get(self, request):

        urls = {
            'Hello World': reverse('Hello World', request=request),
        }

        return Response(urls)


index = IndexView.as_view()


class HelloWorldView(APIView):

    def get(self, request):
        obj = Question.objects.all()

        return Response(data=obj)

    def post(self, request):


        return Response()


hello_world =HelloWorldView.as_view()
