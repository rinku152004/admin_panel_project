from django.urls import path
from . import views
urlpatterns=[
    path('', views.main, name='Main'),
    path('Myapp/',views.member_list,name="Myapp"),
    path('Myapp/details/<int:id>', views.details, name='details'),
    path('testing/', views.testing, name='testing'), 
    # path('test/', views.test, name='test'),
    # path('all_members/',views.member_list,name="member_list"),
]