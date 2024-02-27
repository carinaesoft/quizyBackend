from django.contrib import admin
from .models import Quiz, Category, Tag
from django.db.models import F, Value, Case, When, IntegerField
from mptt.admin import MPTTModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin
# Register your models here.

def assign_common_image(modeladmin, request, queryset):
    common_image_path = '/quiz_images/4.png'  # Specify the path to the common image
    queryset.update(imgSrc=common_image_path)

assign_common_image.short_description = "Assign common image to selected quizzes"

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    ordering = ['name']
    actions = [assign_common_image]

@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    list_display = ['name', 'parent']
    search_fields = ['name']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 10
    list_max_show_all = 100
    list_select_related = True
    list_filter = ['name']



'''
@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['get_full_path', 'get_parent', 'description']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # Annotate categories with a sort_order field.
        # Root categories will have sort_order of 0, all others will have sort_order of 1.
        queryset = queryset.annotate(
            sort_order=Case(
                When(parent__isnull=True, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        )

        # Order by sort_order first, then parent's name, then the category's name.
        return queryset.order_by('sort_order', 'parent__name', 'name')

    def get_parent(self, obj):
        return obj.parent.name if obj.parent else "Główna"

    get_parent.short_description = 'Subcategory of'
'''