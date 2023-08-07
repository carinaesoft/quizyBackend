from django.urls import path
from .views import QuizList, CategoryList, QuizQuestionsAPIView, QuizCreateAPIView, QuestionsAPIView

urlpatterns = [
    path('quiz/', QuizList.as_view(), name='quiz-list'),
    path('quiz/create/', QuizCreateAPIView.as_view(), name='quiz-create'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('quiz/<int:quiz_id>/questions/', QuizQuestionsAPIView.as_view(), name='quiz-questions'),
    path('questions/', QuestionsAPIView.as_view(), name='questions-api'),

]
