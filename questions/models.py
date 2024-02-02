from django.db import models
from quiz.models import Quiz

class Question(models.Model):
    text = models.CharField(max_length=200)
    quizzes = models.ManyToManyField(Quiz)  # ManyToManyField instead of ForeignKey
    created = models.DateTimeField(auto_now_add=True)
    time_limit = models.PositiveIntegerField(default=30)  # Time limit for the question in seconds
    imgSrc = models.ImageField(upload_to='quiz_images/', blank=True)  # Optional image for the question

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answer_set.all()


class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"
