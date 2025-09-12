from django.urls import path
from .views import RecipeListView, welcome, RecipeDetailView
from . import views

app_name = "recipes"

urlpatterns = [
   path("welcome/", welcome, name="welcome"),
   path("list/", RecipeListView.as_view(), name="recipe_list"),
   path('<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),  # recipe details by ID
   path("", views.header_search, name="search_recipes"),        #  current search
   path("advanced-search/", views.advanced_search, name="advanced-search"),  # new one
]
