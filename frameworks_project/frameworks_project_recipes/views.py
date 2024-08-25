import requests
from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DeleteView, DetailView, UpdateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Recipe, Ingredient
from .forms import RecipeDetailForm, MealIDForm, UserRecipeForm
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
                return redirect('your-recipes')

            else:
                # If the API call fails, raise a 404 error
                raise Http404("Failed to retrieve meal from external API")

        # If the form is invalid, raise a 404 error
        raise Http404("Invalid meal ID")   

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

            # Get all ingredients associated with this recipe
            ingredients = Ingredient.objects.filter(recipe=recipe).values_list('ingredient', flat=True)
            ingredients_data = '; '.join(ingredients)

            recipes_data.append({
                'id': recipe.id,
                'recipe': recipe.recipe,
                'category': recipe.category,
                'region': recipe.region,
                'image': recipe.image,
                'youtube': recipe.youtube,
                'ingredients_data': ingredients_data,
            })

        return JsonResponse(recipes_data, safe=False)
    return JsonResponse({'error': 'Unauthorized'}, status=403)


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('your-recipes')

    def test_func(self):
        recipe = self.get_object()
        return recipe.user == self.request.user

    def handle_no_permission(self):
        return redirect('your-recipes')
    
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
class RecipeDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Recipe
    form_class = UserRecipeForm
    template_name = 'recipes/your_recipes_detail.html'
    context_object_name = 'recipe'

    def test_func(self):
        # Ensure that only the owner of the recipe can access and edit the details
        recipe = self.get_object()
        return recipe.user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the ingredients associated with the recipe
        context['ingredients'] = Ingredient.objects.filter(recipe=self.get_object())
        return context
    
class RecipeEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = UserRecipeForm
    template_name = 'recipes/your_recipes_edit.html'
    success_url = reverse_lazy('your-recipes')

    def form_valid(self, form):
        recipe = form.save()

        # Reset and save the ingredients
        Ingredient.objects.filter(recipe=recipe).delete()

        for i in range(len(self.request.POST) // 2):
            ingredient_name = self.request.POST.get(f'ingredient-{i}')
            measure = self.request.POST.get(f'measure-{i}')
            if ingredient_name and measure:
                Ingredient.objects.create(recipe=recipe, ingredient=ingredient_name, measure=measure)
            elif ingredient_name or measure:  # If one is missing
                # Handle validation error
                form.add_error(None, 'Both ingredient and measure fields must be filled out.')
                return self.form_invalid(form)

        return redirect(self.success_url)

    def test_func(self):
        # Ensure the current user is the owner of the recipe
        recipe = self.get_object()
        return self.request.user == recipe.user


