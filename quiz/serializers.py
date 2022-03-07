from django.db.models import Avg, Count
from rest_framework import serializers
from .models import Quiz, Categories


class CaategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ['id', 'name', 'description']