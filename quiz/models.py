from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.core.exceptions import ValidationError

DIFF_CHOICES = (
    ('Łatwy', 'Łatwy'),
    ('Średni', 'Średni'),
    ('Trudny', 'Trudny'),
)


class Category(MPTTModel):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)  # Add a description field
    bgImage = models.ImageField(upload_to='category_images/', blank=True)  # Add an image field
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Quiz(models.Model):
    name = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    required_score_to_pass = models.IntegerField(help_text="required score in %")
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES)
    is_featured = models.BooleanField(default=False)
    imgSrc = models.ImageField(upload_to='quiz_images/', blank=True)  # Add an image field
    tags = models.ManyToManyField('Tag', related_name='quizzes', blank=True)  # Many-to-many field for tags
    play_count = models.IntegerField(default=0)
    description = models.TextField(max_length=500, null=True)  # New description field

    def save(self, *args, **kwargs):
        if self.description and len(self.description) > 500:
            raise ValidationError("Description cannot be more than 500 characters.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}-{self.category}"

    def get_questions(self):
        return self.question_set.all()

    class Meta:
        verbose_name_plural = 'Quizzes'


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
