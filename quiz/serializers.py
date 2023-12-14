from .models import Quiz, Category
from rest_framework import serializers
from django.conf import settings


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
            created_quizzes = Quiz.objects.bulk_create(quizzes)

            # After bulk_create, the created objects don't have their ID if the DB doesn't support it.
            # If you need the IDs, you might need to fetch them from the DB based on some unique attributes.
            # This approach is limited and might not work correctly if there are concurrent writes.

            # Assuming you have some unique field(s) to identify the quizzes.
            # Example: using 'name' and 'category' as unique together.
            created_quizzes = Quiz.objects.filter(
                name__in=[item['name'] for item in validated_data],
                category__in=[item['category'] for item in validated_data]
            )
            return created_quizzes
        else:
            return Quiz.objects.create(**validated_data)
