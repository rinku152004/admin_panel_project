from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("/accounts/register/")

        user = User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(request, "Account created successfully")
        return redirect("/accounts/login/")

    return render(request, "accounts/register.html")

def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/dashboard/")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


@login_required(login_url='/accounts/login/')
def create_admin(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        role_type = request.POST.get("role_type")

        user = User.objects.create_user(
            username=username,
            password=password,
            role_type=role_type
        )

        # Set parent admin and level
        user.parent_admin = request.user
        user.level = request.user.level + 1
        user.save()

        messages.success(request, "Admin created successfully")

        return redirect("/dashboard/admin-tree/")

    return render(request, "accounts/create_admin.html")

@login_required(login_url='/accounts/login/')
def logout_view(request):
    logout(request)
    messages.info(request, 'Logout successfully')
    return redirect('/accounts/login/')

@login_required(login_url='/accounts/login/')
def delete_admin(request, id):

    user = get_object_or_404(User, id=id)

    # Security check
    if user.parent_admin != request.user:
        return redirect('/accounts/')

    user.delete()

    return redirect('/accounts/')


@login_required(login_url='/accounts/login/')
def edit_admin(request, id):

    user = get_object_or_404(User, id=id)
    # Security check
    if user.parent_admin != request.user:
        return redirect('/accounts/')

    if request.method == "POST":
        user.username = request.POST.get('username')
        user.role_type = request.POST.get('role_type')
        user.level = request.POST.get('level')

        user.save()

        return redirect('/accounts/')

    return render(request, "accounts/update_user.html", {"user": user})

@login_required(login_url='/accounts/login/')
def account_list(request):
    users = User.objects.all()
    return render(request, "dashboard/admin_list.html", {"admins": users})