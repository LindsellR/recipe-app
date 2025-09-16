from django.urls import path
from .views import RecipeListView, RecipeDetailView, welcome, header_search, advanced_search

app_name = "recipes"

urlpatterns = [
    path("welcome/", welcome, name="welcome"),
    path("list/", RecipeListView.as_view(), name="recipe_list"),
    path('<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path("", header_search, name="search_recipes"),
    path("advanced-search/", advanced_search, name="advanced-search"),
]
