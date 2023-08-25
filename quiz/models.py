from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

DIFF_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)


'''class Categories(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subcategories')

    def get_indented_name(self):
        prefix = '-' * self.get_depth()
        return f"{prefix} {self.name}"

    def get_depth(self):
        depth = 0
        category = self
        while category.parent:
            depth += 1
            category = category.parent
        return depth

    def get_full_path(self):
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.name}"
        return self.name

    def __str__(self):
        return self.get_indented_name()

    def is_root(self):
        """Check if the category is a root category (has no parent)"""
        return self.parent is None'''



class Category(MPTTModel):
    name = models.CharField(max_length=150)
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

    def __str__(self):
        return f"{self.name}-{self.category}"

    def get_questions(self):
        return self.question_set.all()

    class Meta:
        verbose_name_plural = 'Quiz'
