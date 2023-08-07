from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from quiz.models import Categories, Quiz
from django.urls import reverse
from rest_framework import status
from questions.models import Question, Answer
from rest_framework.test import APITestCase


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


class QuestionAPITestCase(APITestCase):
    def setUp(self):
        self.category = Categories.objects.create(name='Science', description='Science category')
        self.quiz = Quiz.objects.create(name='Science Quiz', category=self.category, number_of_questions=10, time=30,
                                        required_score_to_pass=70, difficulty='easy')

    def test_create_question(self):
        url = reverse('quiz-questions', args=[self.quiz.pk])
        data = {
            'question_text': 'What is the capital of France?',
            'answers': [
                {'text': 'London', 'correct': False},
                {'text': 'Paris', 'correct': True},
                {'text': 'New York', 'correct': False},
                {'text': 'Berlin', 'correct': False},
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.first()
        self.assertEqual(question.text, 'What is the capital of France?')
        self.assertEqual(question.quiz, self.quiz)
        self.assertEqual(question.answer_set.count(), 4)


'''class QuestionsAPITestCase(TestCase):

    def setUp(self):
        # Create some initial data
        self.quiz = Quiz.objects.create(name="Sample Quiz", number_of_questions=5, time=15, required_score_to_pass=70,
                                        difficulty="easy")
        self.question = Question.objects.create(text="Sample Question")
        self.question.quizzes.add(self.quiz)
        Answer.objects.create(text="Sample Answer", correct=True, question=self.question)

        # Endpoint URL
        self.url = reverse('questions-api')

    def test_get_questions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['text'], "Sample Question")
        self.assertEqual(response.data[0]['answers'][0]['text'], "Sample Answer")

    def test_post_question(self):
        data = {
            'question_text': 'New Question',
            'answers': [
                {'text': 'Answer 1', 'correct': True},
                {'text': 'Answer 2', 'correct': False},
            ],
            'quizzes': [self.quiz.id]
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Question.objects.count(), 2)
        new_question = Question.objects.latest('id')
        self.assertEqual(new_question.text, 'New Question')
        self.assertEqual(new_question.answer_set.count(), 2)
'''