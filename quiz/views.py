
from api.serializers import AnswerSerializer
from quiz.models import Quiz, Category
from questions.models import  Answer
from .serializers import QuizSerializer, CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .filter import CategoryFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import JSONParser

from rest_framework.generics import ListAPIView


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter




class QuizDetailAPIView(APIView):
    """
    Retrieve a single quiz by its ID along with all its questions and answers.
    If the quiz does not exist, a 404 not found status is returned.
    """
    def get(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
        except Quiz.DoesNotExist:
            return Response({'message': 'Quiz not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the quiz with context
        quiz_serializer = QuizSerializer(quiz, context={'request': request})

        # Fetch questions associated with this quiz
        questions = quiz.get_questions()
        questions_data = []
        for question in questions:
            answers = Answer.objects.filter(question=question)
            answers_serializer = AnswerSerializer(answers, many=True)

            question_data = {
                'text': question.text,
                'answers': answers_serializer.data
            }
            questions_data.append(question_data)

        return Response({
            'quiz': quiz_serializer.data,
            'questions': questions_data
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
    Return a list of all quizzes. If a 'category' parameter is supplied in the URL,
    the view will return all quizzes belonging to that category and its subcategories.
    If category does not exist it returns an empty response.
    """
    serializer_class = QuizSerializer

    def get_queryset(self):
        category_name = self.request.query_params.get('category', None)

        if category_name:
            try:
                category = Category.objects.get(name=category_name)
                categories = category.get_descendants(include_self=True)
                return Quiz.objects.filter(category__in=categories)
            except Category.DoesNotExist:
                return Quiz.objects.none()
        return Quiz.objects.all()


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


