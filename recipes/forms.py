# search/forms.py
from django import forms

MEAL_TYPE_CHOICES = [
    ("all", "Any meal"),
    ("breakfast", "Breakfast"),
    ("lunch", "Lunch"),
    ("dinner", "Dinner"),
    ("snack", "Snack"),
    ("drink", "Drink"),
    ("dessert", "Dessert"),
]

DIFFICULTY_CHOICES = [
    ("easy", "Easy"),
    ("medium", "Medium"),
    ("hard", "Hard"),
]

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
    title = forms.CharField(
        label="Title",
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
