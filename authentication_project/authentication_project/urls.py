# authentication_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # This will handle all URLs starting with /users/
]

print("Root URLconf loaded")
