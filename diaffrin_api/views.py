from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin, ModelViewSet
from rest_framework.response import Response
import json
from pathlib import Path
import  pandas as pd
from diaffrin_api.models import Entity, Commune
from diaffrin_api.serializers import EntitySerializer, CommuneSerializer
from datetime import datetime
CODE = ["1502021", '1502022', '1502023','1502024','1502025','1502026', '1502027','1502028']

class EntityList(ViewSetMixin,generics.ListCreateAPIView):
    model = Entity
    serializer_class = EntitySerializer
    queryset = Entity.objects.all()

    def create(self, request, *args, **kwargs):
        val = request.data
        print(val)
        writeData(val)
        code = val['code']
        data = val['data']
        if code in CODE:
            serializer = EntitySerializer(data=data, many=isinstance(data, list))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response("OK", status= 200)
        else:
            return Response("KO", status= 200)

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


class EntityViewSet(ModelViewSet):
    serializer_class = EntitySerializer
    queryset = Entity.objects.all()

class ExportProductsAPI(APIView):
    def get(self, request):
        data = Entity.objects.all()
        serializer = EntitySerializer(data, many=True)
        df = pd.DataFrame(serializer.data)
        now = datetime.now()
        file_name = now.strftime("%Y%m%d%H%M%S")
        direct = Path(__file__).resolve().parent.parent
        df.to_csv(f"{direct}/data_export/{file_name}.csv", encoding="UTF-8", index=False)
        return Response("OK", status= 200)


def writeData(content):
        try:
            now = datetime.now()
            code = content['code']
            data = content['data']

            text_name = str(code) + "_"+ now.strftime("%Y%m%d%H%M%S") + ".txt"
            direct = Path(__file__).resolve().parent.parent
            f = open(f"{direct}/data_export/users/"+text_name, 'w')
            f.write(str(content))
            f.close()
            serializer = EntitySerializer(data = data, many=isinstance(data, list))
            if serializer.is_valid():
                df = pd.DataFrame(serializer.validated_data, index=[0])
                excel_name = str(code) + "_" + now.strftime("%Y%m%d%H%M%S") + ".csv"
                df.to_csv(f"{direct}/data_export/users/" + excel_name, encoding="UTF-8", index = False)
        except:
            pass
        return 1

