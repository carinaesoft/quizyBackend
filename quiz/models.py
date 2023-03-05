from django.db import models

DIFF_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)


class Categories(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    def __str__(self):
        return self.name

class Quiz(models.Model):
    name = models.CharField(max_length=120)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    required_score_to_pass = models.IntegerField(help_text="required score in %")
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES)

    def __str__(self):
        return f"{self.name}-{self.category}"

    def get_questions(self):
        return self.question_set.all()

    class Meta:
        verbose_name_plural = 'Quiz'

