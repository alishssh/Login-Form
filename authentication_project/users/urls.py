# users/urls.py


from django.urls import path
from .views import CustomLoginView, register, profile,home_view

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),  
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('home/', home_view, name='home'),
]

