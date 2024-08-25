from django.db import models
from django.contrib.auth.models import User
from django.conf import settings # this was added

class Recipe(models.Model):
    recipe = models.CharField(max_length=250)
    category = models.CharField(max_length=250)
    region = models.CharField(max_length=250)
    instructions = models.TextField()
    image = models.CharField(max_length=250, blank=True, null=True)
    uploaded_image = models.ImageField(upload_to='recipe_pics', blank=True, null=True)  # this was added
    youtube = models.CharField(max_length=250, blank=True, null=True)
    api_id = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
            return self.recipe
    
    # this property was added
    @property
    def display_image_url(self):
        """Return user-uploaded image if available, otherwise use API image, and fallback to default S3 image."""
        if self.uploaded_image:
            return f'{settings.MEDIA_URL}{self.uploaded_image}'  # AWS S3 user-uploaded image
        elif self.image:
            return self.image  # API image URL from the 'image' field
        else:
            return f'{settings.MEDIA_URL}default_recipe_image.jpg'  # Default image on S3

class Ingredient(models.Model):
    ingredient = models.CharField(max_length=250)
    measure = models.CharField(max_length=250)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.ingredient
    
