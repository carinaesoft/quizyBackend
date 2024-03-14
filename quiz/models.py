from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.core.exceptions import ValidationError
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils.translation import gettext_lazy as _

DIFF_CHOICES = (
    ('Easy', _('Łatwy')),
    ('Medium', _('Średni')),
    ('Hard', _('Trudny')),
)

class Category(MPTTModel):
    name = models.CharField(max_length=150, verbose_name=_("Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name=_("Parent"))
    bgImage = models.ImageField(upload_to='categories/original/', verbose_name=_("Background Image"))
    bgImage_small = ImageSpecField(source='bgImage',
                                   processors=[ResizeToFill(100, 100)],
                                   format='WEBP',
                                   options={'quality': 60},
                                   )
    bgImage_medium = ImageSpecField(source='bgImage',
                                    processors=[ResizeToFill(200, 200)],
                                    format='WEBP',
                                    options={'quality': 70},
                                    )
    bgImage_large = ImageSpecField(source='bgImage',
                                   processors=[ResizeToFill(400, 400)],
                                   format='WEBP',
                                   options={'quality': 80},
                                    )

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Quiz(models.Model):
    name = models.CharField(max_length=120, verbose_name=_("Name"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Category"))
    number_of_questions = models.IntegerField(verbose_name=_("Number of Questions"))
    time = models.IntegerField(help_text=_("Duration of the quiz in minutes"), verbose_name=_("Time"))
    required_score_to_pass = models.IntegerField(help_text=_("Required score to pass in %"), verbose_name=_("Required Score to Pass"))
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES, verbose_name=_("Difficulty"))
    is_featured = models.BooleanField(default=False, verbose_name=_("Is Featured"))
    tags = models.ManyToManyField('Tag', related_name='quizzes', blank=True, verbose_name=_("Tags"))
    play_count = models.IntegerField(default=0, verbose_name=_("Play Count"))
    description = models.TextField(max_length=500, null=True, verbose_name=_("Description"))
    imgSrc = models.ImageField(upload_to='quizzes/original/', verbose_name=_("Image Source"))
    imgSrc_small = ImageSpecField(source='imgSrc',
                                  processors=[ResizeToFill(100, 100)],
                                  format='WEBP',
                                  options={'quality': 60},
                                  )
    imgSrc_medium = ImageSpecField(source='imgSrc',
                                   processors=[ResizeToFill(200, 200)],
                                   format='WEBP',
                                   options={'quality': 70},)
    imgSrc_large = ImageSpecField(source='imgSrc',
                                  processors=[ResizeToFill(400, 400)],
                                  format='WEBP',
                                  options={'quality': 80},
                                  )
    def save(self, *args, **kwargs):
        if self.description and len(self.description) > 500:
            raise ValidationError(_("Description cannot be more than 500 characters."))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.category}"

    def get_questions(self):
        return self.question_set.all()

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
