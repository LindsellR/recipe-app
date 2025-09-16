from django.shortcuts import render
from .models import Recipe
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AdvancedSearchForm
from django.db.models import Q
from users.models import Favourite


# Matplotlib imports for charts (use non-GUI backend)
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd

# Create your views here.


def welcome(request):
    return render(request, "recipes/welcome.html")


# recipes/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Recipe


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/main.html"
    context_object_name = "recipes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Get all favourite recipe IDs for this user
            context["fav_ids"] = set(
                Favourite.objects.filter(user=self.request.user)
                .values_list("recipe_id", flat=True)
            )
        else:
            context["fav_ids"] = set()
        return context


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "recipes/details.html"
    context_object_name = "recipe"  # accessible in template as 'recipe'


# Header search
def header_search(request):
    query = request.GET.get("q", "")
    meal_type = request.GET.get("meal_type", "all")

    recipes = Recipe.objects.all()

    if query:
        recipes = recipes.filter(
            Q(name__icontains=query) | Q(ingredients__icontains=query)
        )

    if meal_type and meal_type != "all":
        recipes = recipes.filter(meal_type=meal_type)

    # Add user's favourite recipe IDs to the context
    if request.user.is_authenticated:
        fav_ids = set(
            Favourite.objects.filter(user=request.user)
            .values_list("recipe_id", flat=True)
        )
    else:
        fav_ids = set()

    return render(
        request,
        "recipes/search_results.html",
        {"recipes": recipes, "fav_ids": fav_ids},
    )

# Advanced search page
def advanced_search(request):
    form = AdvancedSearchForm(request.GET or None)
    recipes = Recipe.objects.all()

    if form.is_valid() and request.GET:
        name = form.cleaned_data.get("name")
        ingredient = form.cleaned_data.get("ingredient")
        meal_type = form.cleaned_data.get("meal_type")
        difficulty = form.cleaned_data.get("difficulty")
        max_time = form.cleaned_data.get("max_cooking_time")

        # Apply filters only if field has a value
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

    # Only generate charts and DataFrame if there are recipes
    chart_bar = chart_pie = chart_line = None
    df_html = None
    if recipes.exists():
        df = pd.DataFrame(
            list(
                recipes.values(
                    "id",
                    "name",
                    "ingredients",
                    "meal_type",
                    "difficulty",
                    "cooking_time",
                )
            )
        )
        # Make the recipe name a link to its detail page
        df["name"] = df.apply(
            lambda row: f'<a href="/recipes/{row["id"]}/">{row["name"]}</a>', axis=1
        )
        # Convert DataFrame to HTML for template display
        df_html = df.to_html(classes="advanced-table-search", index=False, escape=False)

    # Generate charts only if there are recipes
    if recipes.exists():
        df = pd.DataFrame(
            list(
                recipes.values("id", "name", "meal_type", "cooking_time", "difficulty")
            )
        )

        # Bar chart: count by meal_type
        meal_counts = df["meal_type"].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.bar(meal_counts.index.astype(str), meal_counts.values, color="#2c6f2c")
        ax1.set_title("Recipes per Meal Type")
        ax1.set_xlabel("Meal Type")
        ax1.set_ylabel("Number of Recipes")
        fig1.tight_layout()
        buf = BytesIO()
        fig1.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        chart_bar = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()
        plt.close(fig1)

        # Pie chart: difficulty distribution
        diff_counts = df["difficulty"].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(
            diff_counts.values,
            labels=diff_counts.index.astype(str),
            autopct="%1.1f%%",
            startangle=140,
        )
        ax2.set_title("Recipe Difficulty Distribution")
        fig2.tight_layout()
        buf = BytesIO()
        fig2.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        chart_pie = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()
        plt.close(fig2)

        # Line chart: cooking time per recipe (sorted)
        df_sorted = df.sort_values("cooking_time")
        fig3, ax3 = plt.subplots()
        ax3.plot(
            df_sorted["name"].astype(str),
            df_sorted["cooking_time"],
            marker="o",
            linestyle="-",
            color="#CBA135",
        )
        ax3.set_title("Cooking Time per Recipe")
        ax3.set_xlabel("Recipe")
        ax3.set_ylabel("Cooking Time (min)")
        ax3.tick_params(axis="x", rotation=45, labelsize=8)
        fig3.tight_layout()
        buf = BytesIO()
        fig3.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        chart_line = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()
        plt.close(fig3)

    # Debug info
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
