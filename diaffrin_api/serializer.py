from rest_framework import serializers


from .models import EntityModel, Paiement
from .constant import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers, status
from rest_framework.views import APIView
from .file_utils import append_to_csv,append_to_txt
from datetime import datetime
class EntitySerializer(serializers.ModelSerializer):
    paiement = serializers.SerializerMethodField()
    impot = serializers.SerializerMethodField()
    class Meta:
        model = EntityModel
        fields = '__all__'

    def get_paiement(self, obj):
        mois = self.context.get("mois")
        annee = self.context.get("annee")
        paiement = obj.get_paiement(mois, annee)
        if paiement: return PaiementSerializer(paiement).data
        return None

    def get_impot(self, obj):
        from .impot_view import ImpotSerializer
        annee = self.context.get("annee")
        impot = obj.get_impot(annee)
        if impot: return ImpotSerializer(paiement).data
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
        entities = EntityModel.objects.filter(property=property_value,locality=locality_value,active=True)
        serializer = EntitySerializer(
            entities,
            many=True,
            context={"mois": mois, "annee": annee})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        append_to_csv("entity_data.csv", request.data)
        serializer = EntitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if serializer.errors:
            append_to_txt("entity_data_errors.txt", serializer.errors, request.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = '__all__'

    def create(self, validated_data):
        entity = validated_data.get("entity_model")
        mois = validated_data.get("mois")
        annee = validated_data.get("annee")
        paiement, created = Paiement.objects.update_or_create(
            entity_model=entity,
            mois=mois,
            annee=annee,
            defaults=validated_data
        )
        return paiement


class PaiementBulkCreateView(APIView):

    def post(self, request):
        mdata = request.data
        append_to_csv("paiement_data.csv", mdata)
        serializer = PaiementSerializer(data=mdata)
        if serializer.is_valid():
            paiement = serializer.save()
            entity_serializer = EntitySerializer(paiement.entity_model,
                context={"mois": paiement.mois, "annee": paiement.annee}
            )
            return Response(entity_serializer.data, status=status.HTTP_201_CREATED)

        append_to_txt("paiement_data_errors.txt", serializer.errors, mdata)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

