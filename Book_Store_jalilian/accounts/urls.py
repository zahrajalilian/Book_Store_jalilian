from django.urls import path
from .views import *
# app_name = 'accounts'

urlpatterns = [
    # path('home/',home,name='home'),
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/',user_profile, name='profile'),
    path('profile/<int:pk>/edit/',UpdateView.as_view(),name='update'),
    # path('change/',views.change_password,name='change'),
]