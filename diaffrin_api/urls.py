from django.urls import path

from . import views

urlpatterns = [
    path("home", views.home, name="home"),
    path('entity/<slug:slug>/', views.get_entity, name="entity_detail")
]