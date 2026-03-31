from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User


# ----------------- UPDATE LEVEL OF CHILD ---------------

def update_child_levels(user):
    children = User.objects.filter(parent_admin=user)

    for child in children:
        child.level = user.level + 1
        child.save()

        update_child_levels(child)

# ---------------- LOGIN ----------------

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user and not user.is_active_admin:
            messages.error(request, "Your account has been disabled.")
            return render(request, "accounts/login.html")

        if user:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("dashboard")

        messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


# ---------------- LOGOUT ----------------

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logout successful")
    return redirect("login")


# ---------------- CREATE ADMIN ----------------

@login_required
def create_admin(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        role_type = request.POST.get("role_type")

        if request.user.role_type == "sub_admin" and role_type != "sub_admin":
            messages.warning(request, "Sub Admin cannot create higher level admins")
            return redirect("create_admin")

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists")
            return redirect("create_admin")

        user = User.objects.create_user(
            username=username,
            password=password,
            role_type=role_type
        )

        user.parent_admin = request.user
        user.level = request.user.level + 1
        user.save()

        messages.success(request, f"{role_type} created successfully")
        return redirect("create_admin")

    return render(request, "accounts/create_admin.html")


# ---------------- DELETE ADMIN ----------------

@login_required
def delete_admin(request, id):

    user = get_object_or_404(User, id=id)

    if request.user.id == user.id:
        messages.error(request, "You cannot delete your own account")
        return redirect("admin_list")

    if request.user != user.parent_admin and request.user.role_type != "super_admin":
        messages.error(request, "You are not allowed to delete this user.")
        return redirect("admin_list")

    children = User.objects.filter(parent_admin=user)

    if user.parent_admin:
        children.update(
            parent_admin=user.parent_admin,
            level=user.parent_admin.level + 1
        )
    else:
        children.update(parent_admin=None, level=0)

    user.delete()
    messages.success(request, "User deleted successfully")

    return redirect("admin_list")


# ---------------- EDIT ADMIN ----------------

@login_required
def edit_admin(request, id):

    user = get_object_or_404(User, id=id)

    if request.user.role_type != "super_admin" and user.parent_admin != request.user:
        messages.error(request, "You don't have permission to edit this user.")
        return redirect("admin_list")

    if user.role_type == "super_admin":
        messages.warning(request, "Super admin cannot be edited.")
        return redirect("admin_list")

    if request.method == "POST":

        user.username = request.POST.get("username")
        user.role_type = request.POST.get("role_type")

        password = request.POST.get("password")

        if password and len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return redirect("edit_admin", id=id)

        if password:
            user.set_password(password)

        parent_id = request.POST.get("parent_admin")

        if parent_id:
            parent_admin = get_object_or_404(User, id=parent_id)

            if parent_admin == user:
                messages.error(request, "User cannot be their own parent.")
                return redirect("edit_admin", id=id)

            parent = parent_admin
            while parent:
                if parent == user:
                    messages.error(request, "Cannot set descendant as parent.")
                    return redirect("edit_admin", id=id)
                parent = parent.parent_admin

            user.parent_admin = parent_admin
            user.level = parent_admin.level + 1

        user.save()

        update_child_levels(user)

        if request.user.id == user.id and password:
            update_session_auth_hash(request, user)

        messages.success(request, "User updated successfully")
        return redirect("admin_list")

    admin_list = User.objects.exclude(id=user.id)

    return render(
        request,
        "accounts/update_user.html",
        {"user": user, "admin_list": admin_list}
    )


# ---------------- TOGGLE STATUS ----------------

@login_required
def toggle_admin_status(request, id):

    user = get_object_or_404(User, id=id)

    if request.user.id == user.id:
        messages.error(request, "You cannot disable your own account.")
        return redirect("admin_list")

    if user.role_type == "super_admin":
        messages.error(request, "Super admin cannot be disabled.")
        return redirect("admin_list")

    if request.user.role_type == "super_admin":
        user.is_active_admin = not user.is_active_admin
        user.save()

    messages.success(request, "User status updated")

    return redirect("admin_list")


# ---------------- DEFAULT ACCOUNTS PAGE ----------------

def accounts_home(request):
    return redirect("admin_list")

