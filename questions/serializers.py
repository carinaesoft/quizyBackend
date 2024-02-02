from rest_framework import serializers
from .models import Question, Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text']  # Excluding 'correct' field

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, source='answer_set', read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers', 'time_limit', 'imgSrc']  # Include new fields
