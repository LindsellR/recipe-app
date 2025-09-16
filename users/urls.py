from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('favourites/add/<int:recipe_id>/', views.add_favourite, name='add_favourite'),
    path('favourites/remove/<int:recipe_id>/', views.remove_favourite, name='remove_favourite'),
    path('favourites/', views.user_favourites, name='user_favourites'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Edit and Delete
    path('recipes/<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipes/<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
]

