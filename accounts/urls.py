from django.urls import path
from . import views

urlpatterns = [
    path('',views.account_list, name='account_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-admin/', views.create_admin, name='create_admin'),
    path('register/', views.register_view, name='register'),
    path('delete/<int:id>/', views.delete_admin, name='delete_admin'),
    path('edit/<int:id>/', views.edit_admin, name='edit_admin'),

]