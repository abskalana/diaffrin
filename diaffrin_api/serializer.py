from rest_framework import serializers
from .models import Entity
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Entity
from django.http import HttpResponse

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'



class EntityBulkCreateView(APIView):

    def post(self, request):
        """
        Expecting a JSON array of entities:
        [
            {"city": "Bamako", "locality": "Quartier A", "meta_user": "admin", "commune": 1, ...},
            {"city": "Segou", "locality": "Quartier B", "meta_user": "admin", "commune": 2, ...}
        ]
        """
        serializer = EntitySerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("true", content_type="text/plain", status=201)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
