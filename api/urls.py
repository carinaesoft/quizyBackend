from django.urls import path
from .views import QuizQuestionsAPIView , QuestionsAPIView


urlpatterns = [
    path('quiz/<int:quiz_id>/questions/', QuizQuestionsAPIView.as_view(), name='quiz-questions'),
    path('questions/', QuestionsAPIView.as_view(), name='questions-api'),
]
