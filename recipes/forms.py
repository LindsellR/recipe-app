# recipes/forms.py
from django import forms
from .models import Recipe

# Choices for dropdown menus in search forms
MEAL_TYPE_CHOICES = [
    ("", "Any meal"),  # Empty string = optional
    ("breakfast", "Breakfast"),
    ("lunch", "Lunch"),
    ("dinner", "Dinner"),
    ("snack", "Snack"),
    ("drink", "Drink"),
    ("dessert", "Dessert"),
]

DIFFICULTY_CHOICES = [
    ("", "Any difficulty"),  # Empty string = optional
    ("easy", "Easy"),
    ("medium", "Medium"),
    ("hard", "Hard"),
]


# --- Create/Update Recipe Form ---
# This is used when adding or editing a recipe.
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "name",
            "ingredients",
            "instructions",
            "meal_type",
            "cooking_time",
            "image_url",
        ]
        widgets = {
            "ingredients": forms.Textarea(
                attrs={"placeholder": "Comma-separated list of ingredients", "rows": 4}
            ),
            "instructions": forms.Textarea(
                attrs={"placeholder": "Step-by-step cooking instructions", "rows": 6}
            ),
            "cooking_time": forms.NumberInput(
                attrs={"placeholder": "Cooking time in minutes"}
            ),
            "image_url": forms.URLInput(
                attrs={"placeholder": "Enter image URL (Optional)"}
            ),
        }


# --- Quick Search Form ---
# Used in the site header for fast lookups by title only.
class RecipeSearchForm(forms.Form):
    title = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Search recipes...", "class": "header-search-input"}
        ),
    )


# --- Advanced Search Form ---
# Used on a dedicated search page with more filter options.
class AdvancedSearchForm(forms.Form):
    name = forms.CharField(
        label="Recipe Name",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search by recipe title"}),
    )
    ingredient = forms.CharField(
        label="Ingredient",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search by ingredient"}),
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
        widget=forms.NumberInput(attrs={"placeholder": "e.g., 30"}),
    )
