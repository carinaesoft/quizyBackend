from .models import Quiz, Category, Tag
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    bgImage = serializers.ImageField(use_url=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    bgImage_small_url = serializers.SerializerMethodField()
    bgImage_medium_url = serializers.SerializerMethodField()
    bgImage_large_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_name', 'description', 'bgImage',
                  'bgImage_small_url', 'bgImage_medium_url', 'bgImage_large_url']

    def get_bgImage_small_url(self, obj):
        return obj.bgImage_small.url if obj.bgImage else None

    def get_bgImage_medium_url(self, obj):
        return obj.bgImage_medium.url if obj.bgImage else None

    def get_bgImage_large_url(self, obj):
        return obj.bgImage_large.url if obj.bgImage else None


from rest_framework import serializers
from .models import Quiz, Category  # Make sure Category is imported if it's used elsewhere in your code

class QuizSerializer(serializers.ModelSerializer):
    category_tree = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    imgSrc_small_url = serializers.SerializerMethodField()
    imgSrc_medium_url = serializers.SerializerMethodField()
    imgSrc_large_url = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'slug', 'number_of_questions', 'time', 'required_score_to_pass',
                  'difficulty', 'category', 'category_tree', 'tags', 'is_featured', 'imgSrc',
                  'imgSrc_small_url', 'imgSrc_medium_url', 'imgSrc_large_url', 'play_count', 'description']

    def get_category_tree(self, obj):
        category = obj.category
        tree = [category.name]
        while category.parent:
            category = category.parent
            tree.append(category.name)
        return tree[::-1]  # Reverse to get the tree from root to leaf

    def get_imgSrc_small_url(self, obj):
        return obj.imgSrc_small.url if obj.imgSrc else None

    def get_imgSrc_medium_url(self, obj):
        return obj.imgSrc_medium.url if obj.imgSrc else None

    def get_imgSrc_large_url(self, obj):
        return obj.imgSrc_large.url if obj.imgSrc else None

    def to_representation(self, instance):
        # Call the original `to_representation` to get the original serialized data
        ret = super().to_representation(instance)
        # Replace the `difficulty` field with its display value
        ret['difficulty'] = instance.get_difficulty_display()
        return ret

    def validate_imgSrc(self, value):
        if not value.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise serializers.ValidationError("Unsupported file type.")
        if value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError("Image file too large ( > 5MB )")
        return value

    def create(self, validated_data):
        if isinstance(validated_data, list):
            quizzes = [Quiz(**item) for item in validated_data]
            created_quizzes = Quiz.objects.bulk_create(quizzes)
            return created_quizzes
        else:
            return Quiz.objects.create(**validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['created_at']  # Assuming you want the created_at timestamp to be read-only
