from django.db import models
from quiz.models import Quiz
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Question(models.Model):
    text = models.CharField(max_length=200)
    quizzes = models.ManyToManyField(Quiz)  # ManyToManyField instead of ForeignKey
    created = models.DateTimeField(auto_now_add=True)
    time_limit = models.PositiveIntegerField(default=30)  # Time limit for the question in seconds
    imgSrc = models.ImageField(upload_to='quiz_images/', blank=True)  # Optional image for the question

    # Define ImageSpecFields for different image sizes
    imgSrc_small = ImageSpecField(source='imgSrc',
                                  processors=[ResizeToFill(100, 100)],
                                  format='WEBP',
                                  options={'quality': 60})
    imgSrc_medium = ImageSpecField(source='imgSrc',
                                   processors=[ResizeToFill(200, 200)],
                                   format='WEBP',
                                   options={'quality': 70})
    imgSrc_large = ImageSpecField(source='imgSrc',
                                  processors=[ResizeToFill(400, 400)],
                                  format='WEBP',
                                  options={'quality': 80})

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
