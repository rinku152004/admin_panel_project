from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from roles.models import Role

@login_required
def home(request):
    return redirect('/dashboard/')


@login_required
def dashboard(request):
    total_users=User.objects.count()
    total_admins=User.objects.filter(role_type="admin").count()
    total_super_admins=User.objects.filter(role_type="super_admin").count()
    total_sub_admins=User.objects.filter(role_type="sub_admin").count()
    total_roles= Role.objects.count()

    context={
        "total_users":total_users,
        "total_super_admins": total_super_admins,
        "total_admins": total_admins,
        "total_sub_admins": total_sub_admins,
        "total_roles": total_roles
    }

    return render(request, "dashboard/dashboard.html",context)


@login_required
def admin_list(request):

    if request.user.role_type == "super_admin":
        admin_list=User.objects.all()
    else:
        admin_list=User.objects.filter(parent_admin=request.user)

    # query = request.GET.get('q')
    # if query:
    #     admin_list = User.objects.select_related('parent_admin').filter(username__icontains=query).order_by('level','id')
    # else:
    #     admin_list = User.objects.select_related('parent_admin').all().order_by('level','id')

    return render(request, "dashboard/admin_list.html", {"admin_list": admin_list})

    # admin_list = User.objects.all().order_by('level','id')

    # return render(request, "dashboard/admin_list.html", {"admin_list": admin_list})

@login_required
def reports(request):

    return render(request, "dashboard/reports.html")


@login_required
def admin_tree(request):

    admin_list = User.objects.filter(parent_admin=None, role_type='super_admin')

    return render(request, "dashboard/admin_tree.html", {"admin_list": admin_list})

