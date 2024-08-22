from django.urls import path
from . import views

urlpatterns = [
    path('our_recipes', views.our_recipes, name='our-recipes'),
]