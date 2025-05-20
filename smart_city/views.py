import pandas as pd
from rest_framework.decorators import  api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Sensor

@api_view(["POST"])
def carregar_planilhas(request):
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

         
       