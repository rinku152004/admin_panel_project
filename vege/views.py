from django.shortcuts import render, redirect
from .models import Recipe

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


def delete_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    
    return redirect('/recipes/')

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