from rest_framework import serializers
from questions.models import Question, Answer
from quiz.models import Quiz, Category




class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('text', 'correct')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(source='answer_set', many=True, read_only=True)
    quizzes = serializers.StringRelatedField(many=True, read_only=True)  # This will show the quiz names

    class Meta:
        model = Question
        fields = ('id', 'text', 'answers', 'quizzes')

