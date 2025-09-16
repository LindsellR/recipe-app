# search/forms.py
from django import forms
from .models import Recipe

MEAL_TYPE_CHOICES = [
    ("", "Any meal"),
    ("breakfast", "Breakfast"),
    ("lunch", "Lunch"),
    ("dinner", "Dinner"),
    ("snack", "Snack"),
    ("drink", "Drink"),
    ("dessert", "Dessert"),
]

DIFFICULTY_CHOICES = [
    ("", "Any difficulty"),
    ("easy", "Easy"),
    ("medium", "Medium"),
    ("hard", "Hard"),
]

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "ingredients", "instructions", "meal_type", "difficulty", "cooking_time", "pic"]
        widgets = {
            "ingredients": forms.Textarea(attrs={"rows": 4}),
            "instructions": forms.Textarea(attrs={"rows": 6}),
        }

# Quick header search form
class RecipeSearchForm(forms.Form):
    title = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Search recipes...",
            "class": "header-search-input"
        })
    )

# Advanced search form for full search page
class AdvancedSearchForm(forms.Form):
    name = forms.CharField(
        label="Recipe Name",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search by recipe title"})
    )
    ingredient = forms.CharField(
        label="Ingredient",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search by ingredient"})
    )
    meal_type = forms.ChoiceField(
        label="Meal Type",
        choices=MEAL_TYPE_CHOICES,
        required=False,
    )
    difficulty = forms.ChoiceField(
        label="Difficulty",
        choices=DIFFICULTY_CHOICES,
        required=False,
    )
    max_cooking_time = forms.IntegerField(
        label="Max Cooking Time (minutes)",
        required=False,
        widget=forms.NumberInput(attrs={"placeholder": "e.g., 30"})
    )

    class RecipeForm(forms.ModelForm):
        class Meta:
            model = Recipe
            fields = ["name", "ingredients", "instructions", "meal_type", "difficulty", "cooking_time", "pic"]

            widgets = {
                "ingredients": forms.Textarea(attrs={"rows": 4}),
                "instructions": forms.Textarea(attrs={"rows": 6}),
            }

