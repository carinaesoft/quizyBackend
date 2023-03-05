from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from quiz.models import Categories, Quiz


class QuizModelTestCase(TestCase):
    def setUp(self):
        self.category = Categories.objects.create(name='Test Category', description='Description for Test Category')
        self.quiz = Quiz.objects.create(name='Test Quiz', category=self.category, number_of_questions=10, time=30,
                                        required_score_to_pass=70, difficulty='easy')

    def test_quiz_model(self):
        self.assertEqual(str(self.quiz), 'Test Quiz-Test Category')
        self.assertEqual(self.quiz.category.name, 'Test Category')
        self.assertEqual(self.quiz.number_of_questions, 10)
        self.assertEqual(self.quiz.time, 30)
        self.assertEqual(self.quiz.required_score_to_pass, 70)
        self.assertEqual(self.quiz.difficulty, 'easy')


class CategoriesModelTestCase(TestCase):
    def setUp(self):
        self.category = Categories.objects.create(
            name='Test Category',
            description='This is a test category'
        )

    def test_category_name(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_category_description(self):
        self.assertEqual(self.category.description, 'This is a test category')
