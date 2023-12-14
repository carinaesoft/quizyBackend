from django.urls import path
from .views import CategoryList, QuizDetailAPIView, QuizList, PopularQuizzesView, QuizCreateAPIView


urlpatterns = [
    # ... other URL patterns ...

    # URL pattern for the QuizDetailAPIView
    path('quiz/<int:quiz_id>/', QuizDetailAPIView.as_view(), name='quiz-detail'),
    path('quiz/create/', QuizCreateAPIView.as_view(), name='quiz-create'),
    path('quiz/popular', PopularQuizzesView.as_view(), name='popular-quizzes'),
    path('quiz/', QuizList.as_view(), name='quiz-list'),
    path('categories/', CategoryList.as_view(), name='category-list'),

]
