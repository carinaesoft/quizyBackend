from game_logic.utilities import (calculate_time_stats, check_answers, generate_feedback, calculate_score, update_game_result, update_question_result)
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.http import JsonResponse

# Assuming you have these models in your application
from quiz.models import Quiz
from questions.models import Question
from results.models import QuestionResult, GameResult
# Create your views here.
import logging

logger = logging.getLogger(__name__)

class QuizSubmitView(APIView):
    def post(self, request, quiz_id):
        game_hash = request.data.get('game_hash')

        try:
            game_result = GameResult.objects.get(game_hash=game_hash)
            question_results = game_result.question_results.all()

            total_questions = question_results.count()
            total_correct = question_results.filter(is_correct=True).count()
            time_taken_list = [qr.time_taken for qr in question_results]

            score = calculate_score(total_correct, total_questions)
            total_time, average_time, fastest_time, longest_time = calculate_time_stats(time_taken_list)

            game_result.score = score
            game_result.average_time_per_question = average_time
            game_result.fastest_response_time = fastest_time
            game_result.longest_response_time = longest_time
            game_result.save()

            return JsonResponse({
                'quiz_id': quiz_id,
                'score': game_result.score,
                'average_time_per_question': average_time,
                'fastest_response_time': fastest_time,
                'longest_response_time': longest_time
            })

        except GameResult.DoesNotExist:
            return JsonResponse({'error': 'GameResult not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class AnswerSubmitView(APIView):
    def post(self, request, question_id):
        game_hash = request.data.get('game_hash')
        user_answers = request.data.get('answers')
        start_time_str = request.data.get('start_time')
        start_time = parse_datetime(start_time_str) if start_time_str else None
        logger.debug("Received start time:", start_time_str)

        quiz_id = request.data.get('quiz_id')  # Get quiz_id from the request data

        if start_time and timezone.is_aware(start_time):
            time_taken = (timezone.now() - start_time).total_seconds()
        else:
            time_taken = None

        if not isinstance(user_answers, list):
            return Response({'error': 'Odpowiedzi muszą być listą.'}, status=400)

        question = get_object_or_404(Question, pk=question_id)
        correct_answers = set(question.get_answers().filter(correct=True).values_list('id', flat=True))
        if not set(user_answers).issubset(set(question.get_answers().values_list('id', flat=True))):
            return Response({'error': 'Przesłane odpowiedzi nie są ważne dla tego pytania.'}, status=400)

        is_correct, partial_correct = check_answers(user_answers, correct_answers)
        feedback = generate_feedback(is_correct, partial_correct)
        time_taken = round(time_taken, 2) if time_taken is not None else None

        correct_answer_ids, incorrect_answer_ids = update_question_result(game_hash, quiz_id, question_id, user_answers, is_correct, time_taken, feedback)

        return Response({
            'question_id': question_id,
            'is_correct': is_correct,
            'feedback': feedback,
            'time_taken': time_taken,
            'correct_answer_ids': correct_answer_ids,
            'incorrect_answer_ids': incorrect_answer_ids
        })

