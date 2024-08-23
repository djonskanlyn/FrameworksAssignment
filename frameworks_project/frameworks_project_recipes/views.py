import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import RecipeDetailForm

@login_required
def our_recipes(request):
    return render(request, 'recipes/our_recipes.html', {'title': 'Recipes'})

@login_required
def our_recipes_detail(request, idMeal):
    url = f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={idMeal}'
    response = requests.get(url)
    meal = response.json()['meals'][0]

    form_data = {
        'idMeal': meal['idMeal'],
        'strMeal': meal['strMeal'],
        'strCategory': meal['strCategory'],
        'strArea': meal['strArea'],
        'strInstructions': meal['strInstructions'],
        'strMealThumb': meal['strMealThumb'],
        'strYoutube': meal['strYoutube']
    }

    # Create form with initial data and pass meal data for dynamic fields
    form = RecipeDetailForm(initial=form_data, meal_data=meal)

    return render(request, 'recipes/our_recipes_detail.html', {'form': form, 'meal': meal})
