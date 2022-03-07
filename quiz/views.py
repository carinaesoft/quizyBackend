from django.shortcuts import render

### REST FRAMEWORK IMPORTS ###

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins

### MODELS ###

from .models import Quiz, Categories

### SERIALIZERS ###

from .serializers import CaategoriesSerializer


# Create your views here.


class Category(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = Categories.objects.all()
    serializer_class = CaategoriesSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
