from django.urls import path
from .views import (
    CategoryList,
    QuizDetailAPIView,
    QuizList,
    PopularQuizzesView,
    QuizCreateAPIView,
    SubcategoryList,
    CategoryDetail,
    list_tags,
    get_quiz_tags,
    QuizListFromCategory
)

urlpatterns = [
    path('quiz/<int:quiz_id>/', QuizDetailAPIView.as_view(), name='quiz-detail'),
    path('quiz/create/', QuizCreateAPIView.as_view(), name='quiz-create'),
    path('quiz/popular', PopularQuizzesView.as_view(), name='popular-quizzes'),
    path('quiz/', QuizList.as_view(), name='quiz-list'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('category/<str:category_name>/', CategoryDetail.as_view(), name='category-detail'),
    path('categoryid/<int:category_id>/', QuizListFromCategory.as_view(), name='category-detail'),
    path('subcategories/<str:category_name>/', SubcategoryList.as_view(), name='subcategory-list'),
    path('tags/', list_tags, name='list_tags'),
    path('quizzes/<int:quiz_id>/tags/get', get_quiz_tags, name='get_quiz_tags'),
]
