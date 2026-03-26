from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from roles.models import Role

@login_required(login_url='/accounts/login/')
def home(request):
    return redirect('/dashboard/')


@login_required(login_url='/accounts/login/')
def dashboard(request):
    total_users=User.objects.count()
    total_admins=User.objects.filter(role_type="admin").count()
    total_roles= Role.objects.count()

    context={
        "total_users":total_users,
        "total_admins": total_admins,
        "total_roles": total_roles
    }

    return render(request, "dashboard/dashboard.html",context)


@login_required(login_url='/accounts/login/')
def admin_list(request):

    admins = User.objects.filter(parent_admin__isnull=False)

    return render(request, "dashboard/admin_list.html", {"admins": admins})

@login_required(login_url='/accounts/login/')
def reports(request):

    return render(request, "dashboard/reports.html")


@login_required(login_url='/accounts/login/')
def admin_tree(request):

    admins = User.objects.filter(parent_admin=None, role_type='super_admin')

    return render(request, "dashboard/admin_tree.html", {"admins": admins})

