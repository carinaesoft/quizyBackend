from django.shortcuts import render
from quiz.models import Quiz, Categories
from api.serializers import QuizSerializer, CategorySerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser


# Create your views here.

class QuizList(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class CategoryList(generics.ListAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
