from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Favourite
from recipes.models import Recipe

#create your views here

@login_required
def add_favourite(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    Favourite.objects.get_or_create(user=request.user, recipe=recipe)
    return redirect(request.META.get('HTTP_REFERER', 'recipes:recipe_list'))

@login_required
def remove_favourite(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    Favourite.objects.filter(user=request.user, recipe=recipe).delete()
    return redirect(request.META.get('HTTP_REFERER', 'recipes:recipe_list'))

@login_required
def user_favourites(request):
    favourites = Favourite.objects.filter(user=request.user)
    return render(request, "favourites/user_favourites.html", {"favourites": favourites})
