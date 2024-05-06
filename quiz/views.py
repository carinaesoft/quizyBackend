# Standard library imports
import uuid

# Related third-party imports
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q
from django.core.exceptions import FieldError,ValidationError

from .serializers import QuizSerializer
# Local application/library-specific imports
from .filter import CategoryFilter
from .serializers import CategorySerializer, QuizSerializer, TagSerializer
from api.serializers import \
    AnswerSerializer  # Assuming this is correct though it looks like it might be a local import as well
from questions.models import Answer, Question
from quiz.models import Category, Quiz, Tag
from quiz.utilities import generate_custom_unique_identifier
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100




# --------------------- Class: CategoryList ---------------------
class CategoryList(generics.ListAPIView):
    """
    Retrieves a list of all categories, allowing filtering by name and ordering.

    **URL:** `/categories/` (GET)

    **Parameters:**
        - `search`: Optional string to filter categories by name (case-insensitive).
        - `ordering`: Optional comma-separated list of fields to order the results.

    **Return:**
        JSON response containing serialized category data.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter


class CategoryDetail(RetrieveAPIView):
    """
    This view retrieves the details of a specific category based on its name.
    The category name is provided in the URL.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'name'

    def get_object(self):
        """
        Overrides the default method to fetch the object based on the category name.
        """
        queryset = self.get_queryset()
        name = self.kwargs.get('category_name')
        return get_object_or_404(queryset, name__iexact=name)


class SubcategoryList(ListAPIView):
    """
    This view returns a list of all subcategories for a given category.
    The category name is provided in the URL.
    """
    serializer_class = CategorySerializer

    def get_queryset(self):
        """
        This view should return a list of all the subcategories
        for the category as determined by the category_name portion of the URL.
        """
        category_name = self.kwargs['category_name']
        # Retrieve the parent category by its name (case insensitive)
        parent_category = get_object_or_404(Category, name__iexact=category_name)
        return Category.objects.filter(parent=parent_category)


class QuizDetailAPIView(APIView):
    """
    Retrieve a single quiz by its ID along with all its question IDs.
    If the quiz does not exist, a 404 not found status is returned.
    """

    def get(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
        except Quiz.DoesNotExist:
            return Response({'message': 'Quiz not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the quiz with context
        quiz_serializer = QuizSerializer(quiz, context={'request': request})

        # Fetch questions associated with this quiz and store their IDs
        questions = quiz.get_questions()
        question_ids = [question.id for question in questions]

        # Generate a unique hash for this response
        game_hash = response_hash = generate_custom_unique_identifier()

        return Response({
            'quiz': quiz_serializer.data,
            'question_ids': question_ids,
            'game_hash': game_hash  # Include the unique hash in the response
        })


class PopularQuizzesView(ListAPIView):
    """
    Return a list of all quizzes ordered by their play count descending.
    An optional 'limit' parameter in the URL can be provided to limit the number of returned quizzes.
    """
    serializer_class = QuizSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned quizzes to a given number,
        by filtering against a `limit` query parameter in the URL.
        """
        queryset = Quiz.objects.all().order_by('-play_count')  # Order by play count
        limit = self.request.query_params.get('limit', None)
        if limit is not None:
            queryset = queryset[:int(limit)]
        return queryset


class QuizList(generics.ListAPIView):
    """
    Return a list of all quizzes, with optional filtering based on category, tags,
    and further filtering based on a specified field (e.g., name or ID).
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Optionally filters the returned quizzes based on category or tags,
        and further filtering based on a specified field (e.g., name or ID).
        """
        queryset = super().get_queryset()
        filter_type = self.request.query_params.get('filter_type')
        filter_field = self.request.query_params.get('filter_field')
        filter_value = self.request.query_params.get('filter_value')
        tags = self.request.query_params.getlist('tags')

        # Handle filtering by tags if 'tags' parameter is present
        if tags:
            tags = [int(tag) for tag in tags]
            queryset = queryset.filter(tags__id__in=tags).distinct()

        # Dynamic filtering based on filter_type, filter_field, and filter_value
        if filter_type and filter_field and filter_value:
            filter_keyword = f"{filter_type}__{filter_field}"
            try:
                queryset = queryset.filter(**{filter_keyword: filter_value})
            except FieldError as e:
                raise ValidationError(f"{filter_keyword} is not a valid field for filtering. Error: {str(e)}")

        # Direct filtering by name if specified directly
        name = self.request.query_params.get('name')
        slug = self.request.query_params.get('slug')
        if name:
            queryset = queryset.filter(name__icontains=name)

        if slug:
            queryset = queryset.filter(slug__exact=slug)

        return queryset


class QuizListFromCategory(ListAPIView):
    """
    This view returns a list of all quizzes for a given category.
    The category ID is provided in the URL.
    """
    serializer_class = QuizSerializer
    pagination_class = StandardResultsSetPagination


    def get_queryset(self):
        """
        This view returns a list of all quizzes for a given category.
        The category_id is provided in the URL.
        """
        category_id = self.kwargs['category_id']
        return Quiz.objects.filter(category_id=category_id)

class QuizCreateAPIView(generics.CreateAPIView):
    """
    Create new Quiz objects. This can handle a single quiz or a list of quizzes.
    If the serializer cannot validate the data, it raises an exception with corresponding error messages.
    """
    serializer_class = QuizSerializer
    parser_classes = [JSONParser]
    queryset = Quiz.objects.none()  # Dummy queryset to satisfy DRF requirements

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        status_code = status.HTTP_201_CREATED if is_many else status.HTTP_200_OK
        return Response(serializer.data, status=status_code, headers=headers)


@api_view(['GET'])
def list_tags(request):
    """
    This view returns a list of all tags.
    """
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_quiz_tags(request, quiz_id):
    """
    This view returns a list of all tags associated with a specific quiz.
    The quiz ID is provided in the URL.
    """
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    tags = quiz.tags.all()
    serializer = TagSerializer(tags, many=True)
    print('test')
    return Response(serializer.data)
