from django.urls import path

from . import views_web

urlpatterns = [
    path('', views_web.home, name='login'),
]