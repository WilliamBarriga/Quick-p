"""
project URL Configuration.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("cbnp.urls"), name="api"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
