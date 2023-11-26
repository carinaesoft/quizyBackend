import django_filters
from quiz.models import  Category

def filter_parent_null(queryset, name, value):
    if value.lower() == 'null':
        return queryset.filter(parent__isnull=True)
    return queryset.filter(**{name: value})

class CategoryFilter(django_filters.FilterSet):
    parent = django_filters.CharFilter(method=filter_parent_null)

    class Meta:
        model = Category
        fields = ['parent']
