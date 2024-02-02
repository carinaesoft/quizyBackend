# game_logic/utilities.py
from results.models import GameResult, QuestionResult
from django.core.exceptions import ObjectDoesNotExist
from quiz.models import Quiz  # Import Quiz model
from questions.models import Question  # Import Question model

def check_answers(user_answers, correct_answers):
    """Check if provided answers are correct and return a correctness status."""
    is_correct = set(user_answers) == set(correct_answers)
    partial_correct = not is_correct and set(user_answers).intersection(set(correct_answers))
    return is_correct, partial_correct

def generate_feedback(is_correct, partial_correct):
    """Generate feedback based on answer correctness."""
    if is_correct:
        return "Wszystkie odpowiedzi są poprawne."
    elif partial_correct:
        return "Niektóre odpowiedzi są poprawne."
    else:
        return "Wszystkie odpowiedzi są niepoprawne."

def calculate_score(total_correct, total_questions):
    """Calculate the quiz score."""
    return (total_correct / total_questions) * 100 if total_questions else 0

def calculate_time_stats(time_taken_list):
    """Calculate total, average, fastest, and longest times from a list of time taken values."""
    if not time_taken_list:
        return 0, 0, 0, 0

    total_time = sum(time_taken_list)
    average_time = total_time / len(time_taken_list)
    fastest_time = min(time_taken_list)
    longest_time = max(time_taken_list)

    return total_time, average_time, fastest_time, longest_time

def update_question_result(game_hash, quiz_id, question_id, user_answers, is_correct, time_taken, feedback):
    try:
        quiz = Quiz.objects.get(pk=quiz_id)  # Retrieve the Quiz instance
        game_result, created = GameResult.objects.get_or_create(
            game_hash=game_hash,
            defaults={
                'quiz': quiz,  # Associate the Quiz instance
                'score': 0,  # Initial values for other fields
                'average_time_per_question': 0,
                'fastest_response_time': 0,
                'longest_response_time': 0
            }
        )
        question = Question.objects.get(pk=question_id)  # Retrieve the Question instance
        correct_answers = list(question.get_answers().filter(correct=True).values_list('id', flat=True))

        question_result, created = QuestionResult.objects.update_or_create(
            game=game_result,
            question=question,
            defaults={
                'time_taken': time_taken,
                'is_correct': is_correct,
                'user_answers': user_answers,
                'feedback': feedback,
                'correct_answers': correct_answers
            }
        )

        incorrect_answers = [ans for ans in user_answers if ans not in correct_answers]

        print(f"QuestionResult {'created' if created else 'updated'}: {question_result}")
        return correct_answers, incorrect_answers
    except ObjectDoesNotExist as e:
        print(f"Error: {e}")
        return [], []



def update_game_result(game_hash, quiz_id, score):
    try:
        quiz = Quiz.objects.get(pk=quiz_id)  # Retrieve the Quiz instance
        game_result, created = GameResult.objects.get_or_create(
            game_hash=game_hash,
            defaults={
                'quiz': quiz,  # Associate the Quiz instance
                'score': score
            }
        )

        # Calculate the time stats based on QuestionResults linked to this game_result
        question_results = game_result.question_results.all()
        time_taken_list = [qr.time_taken for qr in question_results if qr.time_taken is not None]

        if time_taken_list:
            average_time_per_question = sum(time_taken_list) / len(time_taken_list)
            fastest_response_time = min(time_taken_list)
            longest_response_time = max(time_taken_list)
        else:
            average_time_per_question = 0
            fastest_response_time = 0
            longest_response_time = 0

        # Update the GameResult instance with the calculated stats
        game_result.average_time_per_question = average_time_per_question
        game_result.fastest_response_time = fastest_response_time
        game_result.longest_response_time = longest_response_time
        game_result.save()

        return game_result, created
    except ObjectDoesNotExist as e:
        print(f"Error updating game result: {e}")
        return None, False