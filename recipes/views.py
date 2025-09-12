from django.shortcuts import render
from .models import Recipe
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..recipes.forms import AdvancedSearchForm
from ..recipes.forms import RecipeSearchForm, AdvancedSearchForm

# Matplotlib imports for charts (use non-GUI backend)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd

#Create your views here.

def welcome(request):
    return render(request, "recipes/welcome.html")

class RecipeListView(LoginRequiredMixin, ListView):           #class-based view
   model = Recipe                         #specify model
   template_name = 'recipes/main.html'    #specify template
   context_object_name = 'recipes'

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/details.html' 
    context_object_name = 'recipe'         # accessible in template as 'recipe'

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

    # Generate charts only if there are recipes
    chart_bar = chart_pie = chart_line = None
    if recipes.exists():
        # Convert to DataFrame
        df = pd.DataFrame(list(recipes.values('id', 'name', 'meal_type', 'cooking_time', 'difficulty')))

        # Bar chart: count by meal_type
        meal_counts = df['meal_type'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.bar(meal_counts.index.astype(str), meal_counts.values, color='#2c6f2c')
        ax1.set_title('Recipes per Meal Type')
        ax1.set_xlabel('Meal Type')
        ax1.set_ylabel('Number of Recipes')
        fig1.tight_layout()
        buf = BytesIO()
        fig1.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        chart_bar = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig1)

        # Pie chart: difficulty distribution
        diff_counts = df['difficulty'].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(diff_counts.values, labels=diff_counts.index.astype(str), autopct='%1.1f%%', startangle=140)
        ax2.set_title('Recipe Difficulty Distribution')
        fig2.tight_layout()
        buf = BytesIO()
        fig2.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        chart_pie = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig2)

        # Line chart: cooking time per recipe (sorted)
        df_sorted = df.sort_values('cooking_time')
        fig3, ax3 = plt.subplots()
        ax3.plot(df_sorted['name'].astype(str), df_sorted['cooking_time'], marker='o', linestyle='-',
                 color='#CBA135')
        ax3.set_title('Cooking Time per Recipe')
        ax3.set_xlabel('Recipe')
        ax3.set_ylabel('Cooking Time (min)')
        ax3.tick_params(axis='x', rotation=45, labelsize=8)
        fig3.tight_layout()
        buf = BytesIO()
        fig3.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        chart_line = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig3)

    context = {
        'form': form,
        'recipes': recipes,
        'chart_bar': chart_bar,
        'chart_pie': chart_pie,
        'chart_line': chart_line,
    }
    return render(request, "recipes/advanced_search.html", context)
