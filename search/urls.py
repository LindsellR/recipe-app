from django.urls import path
from . import views

app_name = "search"

urlpatterns = [
    path("", views.header_search, name="search_recipes"),        #  current search
    path("advanced-search/", views.advanced_search, name="advanced-search"),  # new one
]
