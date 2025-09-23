from django.urls import path
from .views import RecipeListView, RecipeDetailView, welcome, header_search, advanced_search

app_name = "recipes"

urlpatterns = [
    # Landing page
    path("welcome/", welcome, name="welcome"),


    # Core recipe views
    path("list/", RecipeListView.as_view(), name="recipe_list"),
    path("<int:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),

    # Search views
    path("", header_search, name="search_recipes"),  # root → quick header search
    path("advanced_search/", advanced_search, name="advanced_search"),
]
