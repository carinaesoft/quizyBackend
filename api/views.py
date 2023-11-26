from django.shortcuts import render
from quiz.models import Quiz, Category
from questions.models import Question, Answer
from api.serializers import QuizSerializer, CategorySerializer, QuestionSerializer, MainPageCategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .utils import get_quizzes_for_category
from .filter import CategoryFilter
from rest_framework.permissions import IsAdminUser


class QuizCreateAPIView(generics.CreateAPIView):
    serializer_class = QuizSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):  # If a list of objects was provided
            serializer = self.get_serializer(data=request.data, many=True)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:  # If a single object was provided
            return super().create(request, *args, **kwargs)


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter


class QuizQuestionsAPIView(APIView):
    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(pk=quiz_id)
        questions = quiz.get_questions()
        data = {'questions': []}
        for question in questions:
            answers = question.get_answers()
            answer_texts = [answer.text for answer in answers]
            data['questions'].append({
                'text': question.text,
                'answers': answer_texts
            })
        return Response(data)

    def post(self, request, quiz_id):
        quiz = Quiz.objects.get(pk=quiz_id)
        question_text = request.data.get('question_text')
        answers = request.data.get('answers')

        if not question_text or not answers:
            return Response({'message': 'Question text and answers are required.'}, status=status.HTTP_400_BAD_REQUEST)

        question = Question.objects.create(text=question_text, quiz=quiz)
        for answer_text in answers:
            Answer.objects.create(text=answer_text.get('text'), question=question, correct=answer_text.get('correct'))

        return Response({'message': 'Question created successfully.'}, status=status.HTTP_201_CREATED)


class QuestionsAPIView(APIView):

    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        question_data = request.data

        # Extract data from the request
        question_text = question_data.get('question_text')
        answers_data = question_data.get('answers')
        quizzes_data = question_data.get('quizzes', [])

        # Create the question
        question = Question.objects.create(text=question_text)

        # Associate the question with quizzes
        for quiz_id in quizzes_data:
            try:
                quiz = Quiz.objects.get(pk=quiz_id)
                question.quizzes.add(quiz)
            except Quiz.DoesNotExist:
                pass  # If quiz doesn't exist, we simply skip it

        # Create answers for the question
        for answer_data in answers_data:
            Answer.objects.create(text=answer_data['text'], correct=answer_data['correct'], question=question)

        # Serialize the question data to return in the response
        serializer = QuestionSerializer(question)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class QuizList(generics.ListAPIView):
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


class MainPageData(APIView):

    def get(self, request):
        # Fetch all root categories
        root_categories = Category.objects.filter(parent__isnull=True)

        # For each root category, get all associated quizzes including those in its subcategories
        data = []
        for cat in root_categories:
            quizzes_for_category = get_quizzes_for_category(cat.id)  # This function would resemble your getQuizzesForCategory logic but in Django
            serialized_data = MainPageCategorySerializer({
                'id': cat.id,
                'name': cat.name,
                'quizzes': quizzes_for_category
            })
            data.append(serialized_data.data)

        return Response(data)