from rest_framework import generics
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response
import json
from diaffrin_api.models import Entity, Commune
from diaffrin_api.serializers import EntitySerializer, CommuneSerializer

CODE = ["1502021", '1502022', '1502023','1502024','1502025','1502026', '1502027','1502028']

class EntityList(ViewSetMixin,generics.ListCreateAPIView):
    model = Entity
    serializer_class = EntitySerializer
    queryset = Entity.objects.all()

    def create(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        print(request.data)
        data = json_data['data']
        code = json_data['code']
        if code in CODE:
            serializer = EntitySerializer(data=data, many=isinstance(data, list))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response("OK", status= 200)
        else:
            return Response("-1", status=200)

class CommuneList(ViewSetMixin,generics.ListCreateAPIView):
    model = Commune
    serializer_class = CommuneSerializer
    queryset = Commune.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = CommuneSerializer(data=data, many=isinstance(data, list))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("OK", status= 200)