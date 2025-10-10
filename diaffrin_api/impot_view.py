from rest_framework import serializers
from .file_utils import append_to_csv
from .models import Impot, EntityModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .serializer import EntitySerializer

class ImpotSerializer(serializers.ModelSerializer):
    entity_model = serializers.PrimaryKeyRelatedField(queryset=EntityModel.objects.all())
    class Meta:
        model = Impot
        fields = '__all__'

class ImpotListView(APIView):

   def get(self, request):
       annee = request.GET.get("annee", datetime.today().year)
       centre_value = request.GET.get("centre", "")
       city_value = request.GET.get("city", "")
       status_value = request.GET.get("status", "")
       impots = Impot.objects.all()

       if city_value:
           impots = impots.filter(city=city_value)
       if status:
           impots = impots.filter(status=status_value)
       if centre_value:
           impots = impots.filter(centre=centre_value)

       serializer = ImpotSerializer(impots, many=True)
       return Response(serializer.data)

   def post(self, request):
       append_to_csv("impot_data.csv", request.data)
       serializer = ImpotSerializer(data=request.data)
       if serializer.is_valid():
            instance = serializer.save()
            entity_serializer = EntitySerializer(instance.entity_model, context={ "annee": instance.annee})
            return Response(entity_serializer.data, status=status.HTTP_201_CREATED)

       if serializer.errors:
           append_to_txt("impot_data_errors.txt", serializer.errors, mdata)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

