from django.db import models
from quiz.models import Quiz
from questions.models import Question

class GameResult(models.Model):
    game_hash = models.CharField(max_length=255, unique=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    average_time_per_question = models.FloatField(default=0)
    fastest_response_time = models.FloatField(default=0)
    longest_response_time = models.FloatField(default=0)
    # Additional fields as required

    def __str__(self):
        return f"{self.quiz.name} - {self.game_hash}"

class QuestionResult(models.Model):
    game = models.ForeignKey(GameResult, on_delete=models.CASCADE, related_name='question_results')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    time_taken = models.FloatField()
    user_answers = models.JSONField()  # Stores user's answers as a list of answer IDs
    correct_answers = models.JSONField()  # Stores correct answers as a list of answer IDs
    feedback = models.TextField()
    # Additional fields as required
