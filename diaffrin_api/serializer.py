from rest_framework import serializers
from .models import EntityModel,Paiement
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Paiement
from .file_utils import append_to_csv,append_to_txt


class EntitySerializer(serializers.ModelSerializer):
    status_paiement = serializers.SerializerMethodField()
    class Meta:
        model = EntityModel
        fields = '__all__'

    def get_status_paiement(self, obj):
        return getattr(obj, "status_paiement", None)


class EntityBulkCreateView(APIView):

    def get(self, request):
        annee = request.GET.get("annee")
        mois = request.GET.get("mois")
        property_value = request.GET.get("prop", "PRIVEE")
        locality_value = request.GET.get("loc")
        if property_value == "ESPACE PUBLIC" : locality_value ="Kalana"

        entities = EntityModel.objects.all()

        if property_value:
            entities = entities.filter(property=property_value)

        if locality_value:
            entities = entities.filter(locality=locality_value)

        if annee and annee.isdigit() and mois:
            paiements = Paiement.objects.filter(annee=int(annee), mois=mois)
            paiement_dict = {p.entity_model_id: p.status for p in paiements}

            for e in entities:
                e.status_paiement = paiement_dict.get(e.id, None)
        else:
            for e in entities:
                e.status_paiement = None
        serializer = EntitySerializer(entities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        append_to_csv("entity_data.csv", request.data)
        serializer = EntitySerializer(data=request.data, many=True)
        if serializer.is_valid():
            instances = serializer.save()
            return Response(EntitySerializer(instances, many=True).data, status=status.HTTP_201_CREATED)

        if serializer.errors:
            append_to_txt("entity_data_errors.txt", serializer.errors, request.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = '__all__'


class PaiementBulkCreateView(APIView):
    def post(self, request):
        mdata = request.data
        append_to_csv("paiement_data.csv", mdata)
        serializer = PaiementSerializer(data=mdata, many=True)
        if serializer.is_valid():
            instances = serializer.save()
            return Response(PaiementSerializer(instances, many=True).data, status=status.HTTP_201_CREATED)

        if serializer.errors:
            append_to_txt("paiement_data_errors.txt", serializer.errors, mdata)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

