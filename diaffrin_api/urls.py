from django.urls import path

from diaffrin import settings
from . import views
from django.urls import path, re_path
from django.views.generic.base import RedirectView
from django.views.static import serve

favicon_view = RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)

urlpatterns = [
    path("home", views.home, name="home"),
    path('entity/<slug:slug>/', views.get_entity, name="entity_detail"),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^favicon\.ico$', favicon_view),
]