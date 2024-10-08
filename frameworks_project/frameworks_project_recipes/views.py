import requests
from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, DeleteView, DetailView, UpdateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Recipe, Ingredient
from .forms import RecipeDetailForm, MealIDForm, UserRecipeForm, CreateRecipeForm
from django.contrib.auth.decorators import login_required

@login_required
def our_recipes(request):
    return render(request, 'recipes/our_recipes.html', {'title': 'Our Recipes'})

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
                    # Safely retrieve and strip the ingredient and measure, if they exist
                    ingredient_name = meal.get(f'strIngredient{i}')
                    measure = meal.get(f'strMeasure{i}')

                    # Only strip and save if they are not None
                    if ingredient_name:
                        ingredient_name = ingredient_name.strip()
                    if measure:
                        measure = measure.strip()

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

            # Use the display_image_url method to get the correct image URL
            uploaded_image_url = recipe.uploaded_image.url if recipe.uploaded_image else None

            recipes_data.append({
                'id': recipe.id,
                'recipe': recipe.recipe,
                'category': recipe.category,
                'region': recipe.region,
                'image': recipe.image,
                'uploaded_image': uploaded_image_url,  # Add the uploaded image URL
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
        recipe = form.save(commit=False)  # Don't save yet, we want to make some changes first

        # Handle uploaded image
        if form.cleaned_data['uploaded_image']:
            # If a new image is uploaded, clear the API image field
            if recipe.image:
                recipe.image = None  # Clear the API image URL
        
        recipe.save()  # Now save the recipe with the updated fields

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

class RecipeCreateView(LoginRequiredMixin, View):
    template_name = 'recipes/create_recipe.html'

    def get(self, request, *args, **kwargs):
        # Display an empty form for creating a new recipe
        recipe_form = CreateRecipeForm()
        return render(request, self.template_name, {
            'recipe_form': recipe_form,
        })

    def post(self, request, *args, **kwargs):
        # Handle form submission
        recipe_form = CreateRecipeForm(request.POST, request.FILES)

        # Extract ingredients and measures from POST data
        ingredients = []
        measures = []

        # Loop through POST data to find all ingredient/measure pairs
        for key, value in request.POST.items():
            if key.startswith('ingredient-'):
                ingredients.append(value)
            elif key.startswith('measure-'):
                measures.append(value)

        # Collect dynamically submitted ingredients and measures
        valid_pairs = [
            (ingredient.strip(), measure.strip()) for ingredient, measure in zip(ingredients, measures)
            if ingredient.strip() and measure.strip()
        ]

        if recipe_form.is_valid() and valid_pairs:
            # Save the recipe, link it to the logged-in user
            recipe = recipe_form.save(commit=False)
            recipe.user = request.user
            recipe.save()

            # Save the ingredients linked to the recipe
            for ingredient_name, measure in valid_pairs:
                Ingredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient_name,
                    measure=measure
                )

            # Redirect to the user's recipe list
            return redirect('your-recipes')

        # If validation fails, reload the form with errors
        if not valid_pairs:
            recipe_form.add_error(None, 'At least one valid ingredient and measure pair is required.')

        return render(request, self.template_name, {
            'recipe_form': recipe_form,
            'ingredients': ingredients,
            'measures': measures,
        })

    
