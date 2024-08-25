from django.urls import path
from .views import user_recipes_data, SaveRecipeView, RecipeDeleteView, RecipeDetailView, RecipeEditView
from . import views

urlpatterns = [
    path('our_recipes', views.our_recipes, name='our-recipes'),
    path('our_recipes_detail/<int:idMeal>', views.our_recipes_detail, name='our-recipes-detail'),
    path('save-recipe/', SaveRecipeView.as_view(), name='save-recipe'),
    path('your_recipes/', views.your_recipes, name='your-recipes'),
    path('your-recipes-data/', user_recipes_data, name='user-recipes-data'),
    path('delete-recipe/<int:pk>/', RecipeDeleteView.as_view(), name='delete-recipe'),
    path('user-recipe-detail/<int:pk>/', RecipeDetailView.as_view(), name='user-recipe-detail'),
    path('user-recipe-edit/<int:pk>/', RecipeEditView.as_view(), name='user-recipe-edit'),
]