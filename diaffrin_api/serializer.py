from rest_framework import serializers
from .models import EntityModel,Paiement
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Paiement
from .file_utils import append_to_csv



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
        append_to_csv("entity_data.csv", request.data)
        serializer = EntitySerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response("true", status=status.HTTP_201_CREATED)

        if serializer.errors:
            errors_to_save = [{"field": k, "errors": v} for k, v in serializer.errors.items()]
            append_to_csv("entity_data_errors.csv", errors_to_save)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = '__all__'


class PaiementBulkCreateView(APIView):
    def post(self, request):
        append_to_csv("paiement_data.csv", request.data)
        serializer = PaiementSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response("true", status=status.HTTP_201_CREATED)

        if serializer.errors:
            errors_to_save = [{"field": k, "errors": v} for k, v in serializer.errors.items()]
            append_to_csv("paiement_data_errors.csv", errors_to_save)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

