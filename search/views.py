# search/views.py
from django.shortcuts import render
from .forms import RecipeSearchForm, AdvancedSearchForm
from recipes.models import Recipe

from django.shortcuts import render
from .forms import AdvancedSearchForm

from recipes.models import Recipe

# Header search
def header_search(request):
    q = request.GET.get("q", "")
    meal_type = request.GET.get("meal_type", "all")
    recipes = Recipe.objects.all()

    if q:
        recipes = recipes.filter(name__icontains=q)

    if meal_type != "all":
        recipes = recipes.filter(meal_type=meal_type)

    return render(
        request,
        "search/search_results.html",
        {"recipes": recipes, "query": q, "meal_type": meal_type}
    )

# Advanced search page
def advanced_search(request):
    form = AdvancedSearchForm(request.GET or None)
    recipes = Recipe.objects.all()
    if form.is_valid():
        title = form.cleaned_data.get("title")
        ingredient = form.cleaned_data.get("ingredient")
        meal_type = form.cleaned_data.get("meal_type")
        difficulty = form.cleaned_data.get("difficulty")
        max_time = form.cleaned_data.get("max_cooking_time")

        if title:
            recipes = recipes.filter(name__icontains=title)
        if ingredient:
            recipes = recipes.filter(ingredients__icontains=ingredient)
        if meal_type and meal_type != "all":
            recipes = recipes.filter(meal_type=meal_type)
        if difficulty:
            recipes = recipes.filter(difficulty=difficulty)
        if max_time:
            recipes = recipes.filter(cooking_time__lte=max_time)

    # Charts generation code would go here if recipes exist

    return render(request, "search/advanced_search.html", {"form": form, "recipes": recipes})
