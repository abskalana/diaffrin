from django.urls import path, re_path
from django.views.generic.base import RedirectView
from django.views.static import serve

from diaffrin import settings
from . import views

favicon_view = RedirectView.as_view(url='../static/images/favicon.ico', permanent=True)

urlpatterns = [
    path("", views.home, name="home"),
    path("insert/", views.insert_data, name="insert"),
    path('entity/<slug:slug>/', views.get_entity, name="entity_detail"),
    path('carte/', views.carte, name="entity_carte"),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^favicon\.ico$', favicon_view),
]