from django.urls import path, re_path
from django.views.generic.base import RedirectView
from django.views.static import serve

from diaffrin import settings
from . import views

from .serializer import EntityBulkCreateView

favicon_view = RedirectView.as_view(url='../static/images/favicon.ico', permanent=True)

urlpatterns = [
    path("", views.home, name="home"),
    path('entity/<slug:slug>/', views.get_entity, name="entity_detail"),
    path('operations/add/', views.carte, name="create_mouvement"),
    path('operations/list/', views.carte, name="mouvement_list"),
    path('carte/', views.carte, name="entity_carte"),
    path('api/mobileauth/', views.login_view, name="mobileauth"),
    path('api/entity/create/', EntityBulkCreateView.as_view(), name='entity-create'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^favicon\.ico$', favicon_view),
]