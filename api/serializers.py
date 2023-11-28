from rest_framework import serializers
from quiz.models import Quiz, Category
from questions.models import Question, Answer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'description', 'bgImage']

    # If you want to include the URL of the image rather than the image file path:
    bgImage = serializers.ImageField(use_url=True)

class QuizSerializer(serializers.ModelSerializer):
    category_tree = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'number_of_questions', 'time', 'required_score_to_pass', 'difficulty', 'category', 'category_tree', 'is_featured', 'imgSrc', 'play_count']

    def get_category_tree(self, obj):
        category = obj.category
        tree = [category.name]
        while category.parent:
            category = category.parent
            tree.append(category.name)
        return tree[::-1]  # Reverse to get the tree from root to leaf

    def create(self, validated_data):
        if isinstance(validated_data, list):
            quizzes = [Quiz(**item) for item in validated_data]
            Quiz.objects.bulk_create(quizzes)
            return quizzes
        else:
            return Quiz.objects.create(**validated_data)

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


class MainPageCategorySerializer(serializers.ModelSerializer):
    quizzes = QuizSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'quizzes']