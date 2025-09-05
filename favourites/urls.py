from django.urls import path
from . import views

app_name = "favourites"

urlpatterns = [
    path("add/<int:recipe_id>/", views.add_favourite, name="add_favourite"),
    path("remove/<int:recipe_id>/", views.remove_favourite, name="remove_favourite"),
    path("my/", views.user_favourites, name="user_favourites"),
]
