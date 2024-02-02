from django.shortcuts import render

# Create your views here.
from rest_framework.generics import RetrieveAPIView
from .serializers import QuestionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Question, Answer
from django.shortcuts import get_object_or_404
from django.db.models import Q



class QuestionDetailView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer



