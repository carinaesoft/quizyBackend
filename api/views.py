from quiz.models import Quiz
from questions.models import Question, Answer
from api.serializers import QuestionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import get_quizzes_for_category

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



