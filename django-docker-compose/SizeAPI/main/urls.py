from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('size', views.size, name='size'),
]
