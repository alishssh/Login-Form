# authentication_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('test/', lambda request: HttpResponse("Test route works!")),
#     path('users/', include('users.urls')),
# ]
# print("Root URLconf loaded")
