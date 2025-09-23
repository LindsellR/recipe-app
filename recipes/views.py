from django.shortcuts import render
from .models import Recipe
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AdvancedSearchForm
from django.db.models import Q
from users.models import Favourite

# Matplotlib imports for charts (non-GUI backend for server environments)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd


# Welcome / landing page
def welcome(request):
    return render(request, "recipes/welcome.html")


# Show all recipes in the main page (requires login)
class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/main.html"
    context_object_name = "recipes"

    def get_context_data(self, **kwargs):
        """Add favourite recipe IDs for the logged-in user."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["fav_ids"] = set(
                Favourite.objects.filter(user=self.request.user)
                .values_list("recipe_id", flat=True)
            )
        else:
            context["fav_ids"] = set()
        return context


# Show detailed view of a single recipe
class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/details.html"
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = context["recipe"]
        # Prepare a list of ingredients
        if recipe.ingredients:
            context["ingredients_list"] = [i.strip() for i in recipe.ingredients.split(",")]
        else:
            context["ingredients_list"] = []
        return context


# Simple header search (used in navbar quick search)
def header_search(request):
    query = request.GET.get("q", "")
    meal_type = request.GET.get("meal_type", "all")

    recipes = Recipe.objects.all()

    # Apply text search (name OR ingredients)
    if query:
        recipes = recipes.filter(
            Q(name__icontains=query) | Q(ingredients__icontains=query)
        )

    # Filter by meal type if specified
    if meal_type and meal_type != "all":
        recipes = recipes.filter(meal_type=meal_type)

    # Add user's favourites to context
    fav_ids = set()
    if request.user.is_authenticated:
        fav_ids = set(
            Favourite.objects.filter(user=request.user)
            .values_list("recipe_id", flat=True)
        )

    return render(
        request,
        "recipes/search_results.html",
        {"recipes": recipes, "fav_ids": fav_ids},
    )


# Advanced search with multiple filters + charts
def advanced_search(request):
    form = AdvancedSearchForm(request.GET or None)
    recipes = Recipe.objects.all()

    # Apply filters if form is valid and user submitted values
    if form.is_valid() and request.GET:
        name = form.cleaned_data.get("name")
        ingredient = form.cleaned_data.get("ingredient")
        meal_type = form.cleaned_data.get("meal_type")
        difficulty = form.cleaned_data.get("difficulty")
        max_time = form.cleaned_data.get("max_cooking_time")

        if name:
            recipes = recipes.filter(name__icontains=name)
        if ingredient:
            recipes = recipes.filter(ingredients__icontains=ingredient)
        if meal_type and meal_type != "all":
            recipes = recipes.filter(meal_type=meal_type)
        if difficulty:
            recipes = recipes.filter(difficulty=difficulty)
        if max_time is not None:
            recipes = recipes.filter(cooking_time__lte=max_time)

    # Generate DataFrame for displaying results in table format
    chart_bar = chart_pie = chart_line = None
    df_html = None
    if recipes.exists():
        df = pd.DataFrame(
            list(
                recipes.values(
                    "id", "name", "ingredients", "meal_type", "difficulty", "cooking_time"
                )
            )
        )
        # Make recipe name clickable (link to detail view)
        df["name"] = df.apply(
            lambda row: f'<a href="/recipes/{row["id"]}/">{row["name"]}</a>', axis=1
        )
        df_html = df.to_html(classes="advanced-table-search", index=False, escape=False)

    # Generate charts (only if recipes are found)
    if recipes.exists():
        df = pd.DataFrame(
            list(recipes.values("id", "name", "meal_type", "cooking_time", "difficulty"))
        )

        # --- Bar chart: recipes per meal type ---
        meal_counts = df["meal_type"].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.bar(meal_counts.index.astype(str), meal_counts.values, color="#2c6f2c")
        ax1.set_title("Recipes per Meal Type")
        ax1.set_xlabel("Meal Type")
        ax1.set_ylabel("Number of Recipes")
        fig1.tight_layout()
        buf = BytesIO()
        fig1.savefig(buf, format="png", bbox_inches="tight")
        chart_bar = base64.b64encode(buf.getvalue()).decode("utf-8")
        buf.close()
        plt.close(fig1)

        # --- Pie chart: difficulty distribution ---
        diff_counts = df["difficulty"].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(diff_counts.values, labels=diff_counts.index.astype(str), autopct="%1.1f%%", startangle=140)
        ax2.set_title("Recipe Difficulty Distribution")
        fig2.tight_layout()
        buf = BytesIO()
        fig2.savefig(buf, format="png", bbox_inches="tight")
        chart_pie = base64.b64encode(buf.getvalue()).decode("utf-8")
        buf.close()
        plt.close(fig2)

        # --- Line chart: cooking time per recipe (sorted) ---
        df_sorted = df.sort_values("cooking_time")
        fig3, ax3 = plt.subplots()
        ax3.plot(df_sorted["name"].astype(str), df_sorted["cooking_time"], marker="o", linestyle="-", color="#CBA135")
        ax3.set_title("Cooking Time per Recipe")
        ax3.set_xlabel("Recipe")
        ax3.set_ylabel("Cooking Time (min)")
        ax3.tick_params(axis="x", rotation=45, labelsize=8)
        fig3.tight_layout()
        buf = BytesIO()
        fig3.savefig(buf, format="png", bbox_inches="tight")
        chart_line = base64.b64encode(buf.getvalue()).decode("utf-8")
        buf.close()
        plt.close(fig3)

    # TODO: Replace print() with proper logging before production
    if request.GET:
        print("Form valid:", form.is_valid())
        print("Cleaned data:", form.cleaned_data)
        print("Queryset count:", recipes.count())

    context = {
        "form": form,
        "recipes": recipes,
        "chart_bar": chart_bar,
        "chart_pie": chart_pie,
        "chart_line": chart_line,
        "df_html": df_html,
    }
    return render(request, "recipes/advanced_search.html", context)
