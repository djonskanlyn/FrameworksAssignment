from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def our_recipes(request):
    return render(request, 'recipes/our_recipes.html', {'title': 'Recipes'})