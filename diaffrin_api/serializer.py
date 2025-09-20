from rest_framework import serializers
from .models import EntityModel,Paiement
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityModel
        fields = '__all__'



class EntityBulkCreateView(APIView):

    def get(self, request):
        """
        Retourne toutes les entités
        """
        entities = EntityModel.objects.all()
        serializer = EntitySerializer(entities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
            return Response("true", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Paiement


class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = '__all__'


class PaiementBulkCreateView(APIView):
    def post(self, request):

        serializer = PaiementSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response("true", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

