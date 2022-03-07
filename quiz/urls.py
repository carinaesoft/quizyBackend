from . import views
from django.contrib import admin
from django.urls import path


urlpatterns = [
                #path('cars/' , api_views.cars),
                path('categories/' , views.Category.as_view()),
                #path('cars/<int:pk>/', api_views.CarDetail.as_view()),
               ]