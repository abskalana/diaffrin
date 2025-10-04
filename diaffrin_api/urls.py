from django.urls import path, re_path
from django.views.generic.base import RedirectView
from django.views.static import serve

from diaffrin import settings
from . import views

from .serializer import EntityBulkCreateView,PaiementBulkCreateView

favicon_view = RedirectView.as_view(url='../static/images/favicon.ico', permanent=True)

urlpatterns = [
    path("", views.home, name="home"),

    path('operations/add/', views.create_mouvement, name="mouvement_add"),
    path('operations/list/', views.mouvement_list, name="mouvement_list"),
    path("api/paiement/create/", PaiementBulkCreateView.as_view(), name="paiement-create"),
    path("api/paiement/list/", views.entity_paiements, name="paiement-list"),
    path('api/mobileauth/', views.login_view, name="mobileauth"),
    path('api/entity/create/', EntityBulkCreateView.as_view(), name='entity-create'),
    path('api/entity/list/', EntityBulkCreateView.as_view(), name='entity-list'),
    path('entity/<str:pk>/', views.entity_detail_view, name="entity-detail"),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^favicon\.ico$', favicon_view),
]