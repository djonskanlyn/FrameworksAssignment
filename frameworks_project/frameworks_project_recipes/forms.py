import re
import requests
from django import forms
from .models import Recipe
from django.core.exceptions import ValidationError
from django.conf import settings

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


# Form for the Recipe
class UserRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe', 'category', 'region', 'instructions', 'image', 'youtube']
        widgets = {
            'recipe': forms.TextInput(attrs={'placeholder': 'Recipe Name'}),
            'instructions': forms.Textarea(attrs={'placeholder': 'Instructions'}),
        }

    def clean_youtube(self):
        youtube_url = self.cleaned_data.get('youtube')

        if youtube_url:
            # Step 1: Check if the URL matches YouTube link formats
            regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')
            if not regex.match(youtube_url):
                raise ValidationError("Please enter a valid YouTube URL.")
            
            # Step 2: Extract the video ID
            video_id = self.extract_video_id(youtube_url)
            if not video_id:
                raise ValidationError("Invalid YouTube URL. Could not extract video ID.")

            # Step 3: Validate with YouTube Data API
            if not self.check_video_exists(video_id):
                raise ValidationError("The YouTube video does not exist or is not available.")

        return youtube_url

    def extract_video_id(self, url):
        """
        Extract the video ID from YouTube URLs.
        Example: https://www.youtube.com/watch?v=VIDEO_ID
        """
        long_url_regex = re.compile(r'^.*((youtu.be/)|(v/)|(u/w/)|(embed/)|(watch\?))\??v?=?([^#&?]*).*')
        match = long_url_regex.match(url)
        
        if match:
            return match.group(7)  # Video ID is in group 7
        return None

    def check_video_exists(self, video_id):
        """
        Check if a YouTube video exists using YouTube Data API.
        """
        api_key = settings.YOUTUBE_API_KEY  # Get the API key from settings
        url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=id&key={api_key}'

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4XX, 5XX)
            data = response.json()

            # Check if the video exists
            return data['pageInfo']['totalResults'] > 0
        except requests.RequestException as e:
            # Handle any errors with the API request (e.g., network issues or invalid API key)
            raise ValidationError(f"Error validating YouTube video: {str(e)}")

