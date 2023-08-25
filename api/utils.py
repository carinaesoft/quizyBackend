from quiz.models import Quiz, Category
from questions.models import Question, Answer


def get_quizzes_for_category(category_id):
    # Fetch all subcategories for the given category
    subcategories = Category.objects.filter(parent_id=category_id)

    # Include the main category itself
    all_categories = [category_id] + [cat.id for cat in subcategories]

    # Fetch quizzes associated with these categories
    quizzes = Quiz.objects.filter(category__in=all_categories)

    return quizzes
