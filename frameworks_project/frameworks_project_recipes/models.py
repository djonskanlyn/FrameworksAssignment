from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    recipe = models.CharField(max_length=250)
    category = models.CharField(max_length=250)
    region = models.CharField(max_length=250)
    instructions = models.TextField()
    image = models.CharField(max_length=250, blank=True, null=True)
    youtube = models.CharField(max_length=250, blank=True, null=True)
    api_id = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
            return self.recipe

class Ingredient(models.Model):
    ingredient = models.CharField(max_length=250)
    measure = models.CharField(max_length=250)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.ingredient