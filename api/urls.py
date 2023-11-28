from django.urls import path
from .views import QuizList, PopularQuizzesView ,CategoryList, QuizQuestionsAPIView, MainPageData ,QuizCreateAPIView, QuestionsAPIView


urlpatterns = [
    path('quiz/', QuizList.as_view(), name='quiz-list'),
    path('quizzes/popular', PopularQuizzesView.as_view(), name='popular-quizzes'),
    path('quiz/create/', QuizCreateAPIView.as_view(), name='quiz-create'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('quiz/<int:quiz_id>/questions/', QuizQuestionsAPIView.as_view(), name='quiz-questions'),
    path('questions/', QuestionsAPIView.as_view(), name='questions-api'),
    path('mainpage/', MainPageData.as_view(), name='mainpage-api'),
]
