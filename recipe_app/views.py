from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def welcome_view(request):
    return render(request, "recipes/welcome.html")

def login_view(request):
    error_message = None
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("recipes:recipe_list")  # go to recipe list
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "auth/login.html", {"form": form, "error_message": error_message})

def logout_view(request):
    logout(request)
    return render(request, "auth/success.html")

def about_view(request):
    return render(request, "about.html")

