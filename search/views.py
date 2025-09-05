from django.shortcuts import render
from recipes.models import Recipe

# Create your views here.

def search_recipes(request):
    query = request.GET.get("q")  # ingredient keyword
    meal_type = request.GET.get("meal_type")  # breakfast, lunch, etc.
    
    recipes = Recipe.objects.all()

    if query:
        recipes = recipes.filter(ingredients__icontains=query)

    if meal_type and meal_type != "all":
        recipes = recipes.filter(meal_type=meal_type)

    return render(request, "recipes/main.html", {"recipes": recipes})
