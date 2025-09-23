from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Favourite
from recipes.models import Recipe
from recipes.forms import RecipeForm
from django.contrib.auth.hashers import make_password
from .forms import UserProfileForm
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User

# Define a signup form (can also go in users/forms.py)
from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password_confirm"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created!")
            return redirect("login")
    else:
        form = SignUpForm()
    return render(request, "users/signup.html", {"form": form})


@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("users:profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserProfileForm(instance=user)
    return render(request, "users/edit_profile.html", {"form": form})


# Favourites
@login_required
def add_favourite(request, recipe_id):
    try:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        Favourite.objects.get_or_create(user=request.user, recipe=recipe)
        messages.success(request, f"'{recipe.name}' added to favourites!")
    except Exception as e:
        messages.error(request, "Could not add to favourites. Try again.")
    return redirect("recipes:recipe_list")


@login_required
def remove_favourite(request, recipe_id):
    try:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        Favourite.objects.filter(user=request.user, recipe=recipe).delete()
        messages.success(request, f"'{recipe.name}' removed from favourites!")
    except Exception as e:
        messages.error(request, "Could not remove from favourites. Try again.")
    return redirect("recipes:recipe_list")


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
            messages.success(request, "Recipe added successfully!")
            return redirect("users:my_recipes")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RecipeForm()
    return render(request, "users/add_recipe.html", {"form": form})


@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, created_by=request.user)
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, "Recipe updated successfully!")
            return redirect("users:my_recipes")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RecipeForm(instance=recipe)
    return render(request, "users/add_recipe.html", {"form": form, "is_edit": True})


@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, created_by=request.user)
    if request.method == "POST":
        recipe.delete()
        messages.success(request, "Recipe deleted successfully!")
        return redirect("users:my_recipes")
    return render(request, "users/confirm_delete.html", {"recipe": recipe})
