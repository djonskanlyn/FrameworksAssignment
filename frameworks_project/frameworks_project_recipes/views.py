import requests
from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe, Ingredient
from .forms import RecipeDetailForm, MealIDForm
from django.contrib.auth.decorators import login_required

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


class SaveRecipeView(LoginRequiredMixin, TemplateView):
    template_name = 'our_recipes_detail.html'

    def post(self, request, *args, **kwargs):
        # Get the meal ID from the form submission
        form = MealIDForm(request.POST)

        if form.is_valid():
            meal_id = form.cleaned_data['meal_id']

            # Call the external API using the meal ID
            api_url = f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}'
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()

                # Check if the API response contains a valid meal
                if data['meals'] is None:
                    raise Http404("Meal not found")

                meal = data['meals'][0]  # Access the first meal object
                
                # Check if this meal has already been saved in the database
                recipe = Recipe.objects.filter(api_id=meal['idMeal']).first()
                if recipe:
                    # If the recipe already exists, redirect to its detail view
                    return redirect('our-recipes-detail', idMeal=recipe.api_id)

                # Save the recipe details into the database
                recipe = Recipe.objects.create(
                    recipe=meal['strMeal'],
                    category=meal['strCategory'],
                    region=meal['strArea'],
                    instructions=meal['strInstructions'],
                    image=meal['strMealThumb'],
                    youtube=meal['strYoutube'],
                    api_id=meal['idMeal'],
                    user=request.user
                )

                # Save the ingredients related to this recipe
                for i in range(1, 21):  # Maximum of 20 ingredients
                    ingredient_name = meal[f'strIngredient{i}'].strip()
                    measure = meal[f'strMeasure{i}'].strip()

                    # Only save ingredient and measure if both are non-empty and non-whitespace
                    if ingredient_name and measure:
                        Ingredient.objects.create(
                            recipe=recipe,
                            ingredient=ingredient_name,
                            measure=measure
                        )

                # Redirect to a success page or detail view
                return redirect('our-recipes')

            else:
                # If the API call fails, raise a 404 error
                raise Http404("Failed to retrieve meal from external API")

        # If the form is invalid, raise a 404 error
        raise Http404("Invalid meal ID")
    
# # Class-based view for rendering the your_recipes.html template
# class UserRecipesView(LoginRequiredMixin, TemplateView):
#     template_name = 'your_recipes.html'


@login_required
def your_recipes(request):
    return render(request, 'recipes/your_recipes.html', {'title': 'Your Recipes'})

# View to serve user's saved recipes with ingredients aggregated
def user_recipes_data(request):
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(user=request.user)

        # Prepare the data for each recipe (without ingredients)
        recipes_data = []
        for recipe in recipes:
            recipes_data.append({
                'id': recipe.id,
                'recipe': recipe.recipe,
                'category': recipe.category,
                'region': recipe.region,
                'image': recipe.image,
            })

        return JsonResponse(recipes_data, safe=False)
    return JsonResponse({'error': 'Unauthorized'}, status=403)