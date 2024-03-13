from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'entity', views.EntityList, basename='entity')
router.register(r'commune', views.CommuneList, basename='commune')

urlpatterns = [

    path('', include(router.urls)),
]