from django.urls import path
from .views import QuizList, CategoryList

urlpatterns = [
    path('quiz/', QuizList.as_view(), name='quiz-list'),
    path('categories/', CategoryList.as_view(), name='category-list'),
]