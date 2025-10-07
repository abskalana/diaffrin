from rest_framework import serializers
from .models import EntityModel, Paiement
from constant import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers, status
from rest_framework.views import APIView
from .file_utils import append_to_csv,append_to_txt
from datetime import datetime
class EntitySerializer(serializers.ModelSerializer):
    paiement = serializers.SerializerMethodField()
    class Meta:
        model = EntityModel
        fields = '__all__'

    def get_paiement(self, obj):
        mois = self.context.get("mois")
        annee = self.context.get("annee")
        paiement = obj.get_paiement(mois, annee)
        if paiement: return PaiementSerializer(paiement).data
        return None


class EntityBulkCreateView(APIView):

    def get(self, request):
        now = datetime.today()
        annee = request.GET.get("annee", now.year)
        if not annee : annee = now.year
        annee = int(annee)
        mois = request.GET.get("mois",None)
        if not mois : mois = MOIS_MAP[now.month]
        property_value = request.GET.get("prop", "ESPACE PUBLIC")
        locality_value = request.GET.get("loc","Kalana")
        entities = EntityModel.objects.filter(property=property_value,locality=locality_value)
        serializer = EntitySerializer(
            entities,
            many=True,
            context={"mois": mois, "annee": annee})
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
        mois = None
        annee = None
        entities_to_update = []
        if serializer.is_valid():
            instances = serializer.save()
            for i in instances:
                mois = i.mois
                annee = i.annee
                entities_to_update.append(i.entity_model)
            entity_serializer = EntityModelSerializer(entities, many=True,context={"mois": mois, "annee": annee})
            return Response(entity_serializer.data, status=status.HTTP_201_CREATED)

        if serializer.errors:
            append_to_txt("paiement_data_errors.txt", serializer.errors, mdata)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

