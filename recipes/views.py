from django.shortcuts import render
from .models import Recipe
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

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