from .models import Quiz, Category
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    bgImage = serializers.ImageField(use_url=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_name', 'description', 'bgImage']

class QuizSerializer(serializers.ModelSerializer):
    category_tree = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)  # Adding description field with limit

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'number_of_questions', 'time', 'required_score_to_pass', 'difficulty', 'category', 'category_tree', 'is_featured', 'imgSrc', 'play_count', 'description']

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
            created_quizzes = Quiz.objects.bulk_create(quizzes)
            return created_quizzes
        else:
            return Quiz.objects.create(**validated_data)