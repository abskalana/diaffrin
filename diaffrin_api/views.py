from rest_framework import generics
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response

from diaffrin_api.models import Entity
from diaffrin_api.serializers import EntitySerializer

class EntityList(ViewSetMixin,generics.ListCreateAPIView):
    model = Entity
    serializer_class = EntitySerializer
    queryset = Entity.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = EntitySerializer(data=data, many=isinstance(data, list))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("OK", status= 200)