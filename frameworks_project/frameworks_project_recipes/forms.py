from django import forms

class RecipeDetailForm(forms.Form):
    idMeal = forms.CharField(label='Meal ID', disabled=True)
    strMeal = forms.CharField(label='Meal Name', disabled=True)
    strCategory = forms.CharField(label='Category', disabled=True)
    strArea = forms.CharField(label='Region', disabled=True)
    strInstructions = forms.CharField(label='Instructions', widget=forms.Textarea, disabled=True)
    strMealThumb = forms.URLField(label='Meal Thumbnail', disabled=True)
    strYoutube = forms.URLField(label='YouTube Link', required=False, disabled=True)

    def __init__(self, *args, **kwargs):
        meal_data = kwargs.pop('meal_data', None)  # Pop the meal data
        super(RecipeDetailForm, self).__init__(*args, **kwargs)

        # Create a list to store ingredient/measurement pairs
        self.ingredients = []

        # Dynamically add ingredient and measurement fields
        if meal_data:
            for i in range(1, 21):  # TheMealDB provides up to 20 ingredients
                ingredient = meal_data.get(f'strIngredient{i}')
                measure = meal_data.get(f'strMeasure{i}')

                if ingredient and ingredient.strip():  # Only add fields if an ingredient exists
                    # Store ingredient and measure pairs in the list
                    self.ingredients.append({
                        'ingredient': ingredient,
                        'measure': measure if measure else ''
                    })

class MealIDForm(forms.Form):
    meal_id = forms.CharField(max_length=20, widget=forms.HiddenInput())