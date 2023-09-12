
from django.contrib import admin
from rest_framework.authtoken.views import ObtainAuthToken
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('auth/', ObtainAuthToken.as_view()),
]
