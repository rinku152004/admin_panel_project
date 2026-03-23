from django.urls import path
from . import views

urlpatterns = [

    path('recipes/', views.recipes),
    path('delete_recipe/<id>/', views.delete_recipe),
    path('update_recipe/<id>/', views.update_recipe),
    # path('login/',views.login_page),
]