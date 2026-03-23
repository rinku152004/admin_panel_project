from django.shortcuts import render, redirect
# from full_system_application import User
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def recipes(request):

    queryset = Recipe.objects.all()

    if request.method == "POST":
        recipe_name = request.POST.get('recipe_name')
        recipe_ingredients = request.POST.get('recipe_ingredients')
        recipe_description = request.POST.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')

        Recipe.objects.create(
            recipe_name=recipe_name,
            recipe_ingredients=recipe_ingredients,
            recipe_description=recipe_description,
            recipe_image=recipe_image
        )

        return redirect('/recipes/')

    # SEARCH
    if request.GET.get('search'):
        queryset = queryset.filter(recipe_name__icontains=request.GET.get('search'))

    context = {'recipes': queryset}

    return render(request, "add_recipes.html", context)

@login_required(login_url='/login/')
def delete_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    
    return redirect('/recipes/')

@login_required(login_url='/login/')
def update_recipe(request, id):

    queryset = Recipe.objects.get(id=id)

    if request.method == "POST":
        queryset.recipe_name = request.POST.get('recipe_name')
        queryset.recipe_ingredients = request.POST.get('recipe_ingredients')
        queryset.recipe_description = request.POST.get('recipe_description')

        if request.FILES.get('recipe_image'):
            queryset.recipe_image = request.FILES.get('recipe_image')

        queryset.save()
    
        return redirect('/recipes/')

    context = {'recipe': queryset}

    return render(request, "update_recipe.html", context)

def login_page(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request, 'Invalid Username')
            return redirect('/login/')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login/')
        else:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('/recipes/')

        # if user:
        #     if user.check_password(password):
        #         messages.info(request, 'Login successful')
        #         return redirect('/recipes/')
        #     else:
        #         messages.info(request, 'Incorrect password')
        #         return redirect('/login/')
        # else:
        #     messages.info(request, 'User does not exist')
        #     return redirect('/login/')

    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    messages.info(request, 'Logout successful')
    return redirect('/login/')

def register(request):

    if request.method =="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user:
            # User already exists
            messages.info(request, 'Username already exists')
            return redirect('/register/')

        user=User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()
        messages.info(request, 'Account created successfully')
        return redirect('/register/')
    return render(request, 'register.html')