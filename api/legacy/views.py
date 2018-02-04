from api import settings
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse

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
        session = request.db_session

        return Response()

    def post(self, request):


        return Response()


hello_world =HelloWorldView.as_view()
