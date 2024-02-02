from django.urls import path
from .views import QuestionDetailView

urlpatterns = [
    # ... your other URL patterns
    path('<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),


]
