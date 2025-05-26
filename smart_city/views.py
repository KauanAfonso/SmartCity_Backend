import pandas as pd
from rest_framework.decorators import  api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Sensor
from django.shortcuts import get_object_or_404
from .serializers import SensorSerializer

@api_view(["POST"])
def upload_sheets(request):
    if request.method == "POST":
        try:
            planilha = request.FILES['planilha']
        except:
            return Response({"Erro": "Aconteceu algum erro para ler a planilha."}, status=status.HTTP_409_CONFLICT)
        
        try:
            df = pd.read_excel(planilha)

            colunas_nescessarias = ["sensor", "mac_address", "unidade_medida", "longitude", "status", "Kauan"]

            # Verifica se todas as colunas estão presentes no dataframe
            if not all(coluna in df.columns for coluna in colunas_nescessarias):
                return Response({"Erro": "A planilha não contém as colunas necessárias."}, status=status.HTTP_400_BAD_REQUEST)

            for index, row, in df.iterrows():
                dados = Sensor(
                    sensor=row['sensor'],
                    mac_address=row['mac_address'],
                    unidade_med=row['unidade_medida'],
                    latitude = row['latitude'],
                    longitude=row["longitude"],
                    status=row["status"],
                    )
                dados.save()
            return Response({"Mensagem": "Dados criados com sucesso"}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"Mensagem": f"Erro: {e}"}, status=status.HTTP_400_BAD_REQUEST)    


'''

CRUD para lidar com os sensores

'''         
@api_view(["GET", "POST", "PUT", "DELETE"])
def handle_sensor(request, pk=None):
        #Obter um sensor em espécifico ou todos de uma vez !
        if request.method == "GET":
            if pk is not None:
                dados = get_object_or_404(Sensor, pk=pk)
                serializer = SensorSerializer(dados, many=False)
                return Response({"Dados": serializer.data}, status=status.HTTP_200_OK)
            dados = Sensor.objects.all()
            serializer = SensorSerializer(dados, many=True)
            return Response({"Dados": serializer.data}, status=status.HTTP_200_OK)

        #Criar um sensor novo e salvar no banco
        elif request.method == "POST":
            dados = request.data
            serializer = SensorSerializer(data=dados)
            if serializer.is_valid():
                serializer.save()
                return Response({"Mensagem": "Sensor registrado com sucesso !"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #Atualizar um sensor específico
        elif request.method == "PUT":
            if pk is not None:
                sensor = get_object_or_404(Sensor, pk=pk)
                dados = request.data
                serializer = SensorSerializer(sensor, data=dados)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"Mensagem": "Sensor atualizado com sucesso !"},status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        #Deletar um sensor específico
        elif request.method == "DELETE":
            if pk is not None:
                sensor = get_object_or_404(Sensor, pk=pk)
                sensor.delete()
                return Response({"Mensagem": "Sensor Excluido com sucesso !"},status=status.HTTP_200_OK)
            return Response({"Mensagem": "Erro ao encontrar !"}, status=status.HTTP_400_BAD_REQUEST)        
    

            
