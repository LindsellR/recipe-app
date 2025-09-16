from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Favourite
from recipes.models import Recipe
from recipes.forms import RecipeForm
from django.contrib.auth.hashers import make_password
from .forms import UserProfileForm


@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            # only update password if provided
            if form.cleaned_data['password']:
                user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'users/edit_profile.html', {'form': form})

# Favourites
@login_required
def add_favourite(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    Favourite.objects.get_or_create(user=request.user, recipe=recipe)
    return redirect('recipes:recipe_list')  # always go to main recipe list

@login_required
def remove_favourite(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    Favourite.objects.filter(user=request.user, recipe=recipe).delete()
    return redirect('recipes:recipe_list')  # always go to main recipe list


@login_required
def user_favourites(request):
    favourites = Favourite.objects.filter(user=request.user)
    return render(request, "users/user_favourites.html", {"favourites": favourites})

# Profile
@login_required
def profile(request):
    return render(request, "users/profile.html")

# User recipes
@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(created_by=request.user)
    return render(request, "users/my_recipes.html", {"recipes": recipes})

@login_required
def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            return redirect("users:my_recipes")
    else:
        form = RecipeForm()
    return render(request, "users/add_recipe.html", {"form": form})

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, created_by=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('users:my_recipes')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'users/add_recipe.html', {'form': form})

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, created_by=request.user)
    if request.method == 'POST':
        recipe.delete()
        return redirect('users:my_recipes')
    return render(request, 'users/confirm_delete.html', {'recipe': recipe})
