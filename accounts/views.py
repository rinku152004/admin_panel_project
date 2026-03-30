from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# from admin_panel_project.dashboard.views import dashboard
# from urllib3 import request
from .models import User


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user and not user.is_active_admin:
            messages.error(request, "Your account has been disabled.")
            return render(request, "accounts/login.html")


        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "accounts/login.html")

    return render(request, "accounts/login.html")


@login_required
def create_admin(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        role_type = request.POST.get("role_type")

        # Security check: Sub Admin cannot create higher level admins
        if request.user.role_type == "sub_admin" and role_type != "sub_admin":
            messages.error(request, "Sub Admin cannot create higher level admins")
            return redirect("/accounts/create_admin/")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("/accounts/create_admin/")

        user = User.objects.create_user(
            username=username,
            password=password,
            role_type=role_type
        )

        # Set parent admin and level
        user.parent_admin = request.user
        user.level = request.user.level + 1
        user.save()

        messages.success(request, f"{user.role_type} created successfully")

        return redirect("/accounts/create_admin/")

    return render(request, "accounts/create_admin.html")

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Logout successfully')
    return redirect('/accounts/login/')

@login_required
def delete_admin(request, id):

    user = get_object_or_404(User, id=id)

    if request.user.id == user.id:
            messages.error(request, "You cannot delete your own account")
            return redirect('/accounts/')

    # Security check: Only parent admin or super admin can delete
    if request.user == user.parent_admin or request.user.role_type == "super_admin":

        # Check if the admin has sub-admins before deleting
        # if user.objects.filter(parent_admin=user).exists():
        #     messages.error(request, "Cannot delete admin with sub-admins.")
        #     return redirect('/accounts/')

        # Reassign sub-admins to the parent admin before deleting
        children=User.objects.filter(parent_admin=user)
        if user.parent_admin:
            children.update(parent_admin=user.parent_admin, level=user.parent_admin.level+1)
        else:
            children.update(parent_admin=None, level=0)

        user.delete()
        return redirect('/accounts/')
    else:
        messages.error(request, "You are not the parent admin of this user.")
        return redirect('/accounts/')


@login_required
def edit_admin(request, id):

    user = get_object_or_404(User, id=id)

    # Security check
    if request.user.role_type != "super_admin" and user.parent_admin != request.user:
        messages.error(request, "You don't have permission to edit this user.")
        return redirect('/dashboard/admins/')

    # Prevent editing super admin
    if user.role_type == "super_admin":
        messages.error(request, "Super admin cannot be edited.")
        return redirect('/dashboard/admins/')

    if request.method == "POST":

        parent_id = request.POST.get('parent_admin')
        if parent_id:
            parent_admin = get_object_or_404(User, id=parent_id)
            
            # Prevent setting self as parent
            if parent_admin == user:
                messages.error(request, "User cannot be their own parent.")
                return redirect(f'/accounts/edit/{id}/')

            parent=parent_admin
            while parent:
                if parent == user:
                    messages.error(request, "Cannot set a descendant as parent.")
                    return redirect(f'/accounts/edit/{id}/')
                parent = parent.parent_admin

            # if parent_admin.role_type == "super_admin" or parent_admin == request.user:
            user.parent_admin = parent_admin
            user.level = parent_admin.level + 1
            # else:
            #     messages.error(request, "Parent admin must be a super admin or your direct parent.")
            #     return redirect(f'/accounts/edit/{id}/')
            
        user.username = request.POST.get('username')
        user.role_type = request.POST.get('role_type')

        password = request.POST.get('password')

        if password:
            user.set_password(password)

        user.save()

        messages.success(request, "User updated successfully")

        return redirect('/dashboard/admins/')

    admins = User.objects.exclude(id=user.id)
    return render(request, "accounts/update_user.html", {"user": user, "admins": admins})



@login_required
def toggle_admin_status(request, id):

    user = get_object_or_404(User, id=id)

    # Prevent disabling yourself
    if request.user.id == user.id:
        messages.error(request, "You cannot disable your own account.")
        return redirect('/dashboard/admins/')

    # Prevent disabling super admin
    if user.role_type == "super_admin":
        messages.error(request, "Super admin cannot be disabled.")
        return redirect('/dashboard/admins/')

    if request.user.role_type == "super_admin":
        user.is_active_admin = not user.is_active_admin
        user.save()

    return redirect('/dashboard/admins/')

from django.shortcuts import redirect

def accounts_home(request):
    return redirect('/dashboard/admins/')