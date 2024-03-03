from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Question, Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text']  # Excluding 'correct' field

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, source='answer_set', read_only=True)
    imgSrc_small_url = serializers.SerializerMethodField()
    imgSrc_medium_url = serializers.SerializerMethodField()
    imgSrc_large_url = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers', 'time_limit', 'imgSrc',
                  'imgSrc_small_url', 'imgSrc_medium_url', 'imgSrc_large_url']

    def get_imgSrc_small_url(self, obj):
        if obj.imgSrc and hasattr(obj.imgSrc_small, 'url'):
            return obj.imgSrc_small.url
        return None

    def get_imgSrc_medium_url(self, obj):
        if obj.imgSrc and hasattr(obj.imgSrc_medium, 'url'):
            return obj.imgSrc_medium.url
        return None

    def get_imgSrc_large_url(self, obj):
        if obj.imgSrc and hasattr(obj.imgSrc_large, 'url'):
            return obj.imgSrc_large.url
        return None

    def validate_imgSrc(self, value):
        # Validate file type
        if not value.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise serializers.ValidationError("Unsupported file type. Only JPG and PNG are allowed.")

        # Validate file size (e.g., no larger than 5MB)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image file too large. Size should not exceed 5MB.")

        return value
