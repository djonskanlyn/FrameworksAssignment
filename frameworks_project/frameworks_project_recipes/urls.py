from django.urls import path
from . import views

urlpatterns = [
    path('our_recipes', views.our_recipes, name='our-recipes'),
    path('our_recipes_detail/<int:idMeal>', views.our_recipes_detail, name='our-recipes-detail'),
]