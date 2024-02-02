from django.urls import path
from .views import QuizSubmitView, AnswerSubmitView

urlpatterns = [
    path('quiz/submit/<int:quiz_id>/', QuizSubmitView.as_view(), name='quiz-submit'),
    path('question/submit/<int:question_id>/', AnswerSubmitView.as_view(), name='answer-submit'),
]