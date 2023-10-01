from django.urls import include, path
from rest_framework import routers

from . import views
from .views import ExportProductsAPI

router = routers.DefaultRouter()
router.register(r'entity', views.EntityList, basename='entity')

router.register(r'commune', views.CommuneList, basename='commune')

urlpatterns = [
    path('api/export', ExportProductsAPI.as_view(),name='export'),
    path('', include(router.urls)),
]