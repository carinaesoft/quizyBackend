from django.contrib import admin
from results.models import QuestionResult, GameResult


@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = ('game_hash', 'quiz', 'score', 'average_time_per_question', 'fastest_response_time', 'longest_response_time')
    list_filter = ('quiz',)
    search_fields = ('game_hash', 'quiz__name')
@admin.register(QuestionResult)
class QuestionResultAdmin(admin.ModelAdmin):
    list_display = ('game', 'question', 'is_correct', 'time_taken', 'display_user_answers', 'display_correct_answers')
    list_filter = ('game', 'question', 'is_correct')
    search_fields = ('game__game_hash', 'question__text')

    def display_user_answers(self, obj):
        return ", ".join(str(answer) for answer in obj.user_answers)
    display_user_answers.short_description = 'User Answers'

    def display_correct_answers(self, obj):
        return ", ".join(str(answer) for answer in obj.correct_answers)
    display_correct_answers.short_description = 'Correct Answers'
