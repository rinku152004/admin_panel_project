from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.accounts_home),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_admin/', views.create_admin, name='create_admin'),
    # path('register/', views.register_view, name='register'),
    path('delete/<int:id>/', views.delete_admin, name='delete_admin'),
    path('edit/<int:id>/', views.edit_admin, name='edit_admin'),
    path('toggle-admin/<int:id>/', views.toggle_admin_status, name='toggle_admin'),
]