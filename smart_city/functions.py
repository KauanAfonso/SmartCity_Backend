from .models import Sensor, Ambiente, Historico
import pandas as pd
from rest_framework.response import Response
from rest_framework import status

'''
FUNÇÔES

Essa função tem o objetivo de verificar as colunas nescessarias para realizar o upload das informações
no banco. Verificam se estão todas presentes na planilha e cria um objeto para o banco.
O parametro dessas funções são o df, ou seja a planilha que está sendo lendo no momento. Essas
funções serão utilizadas na ./view.py/upload_sheets
-------------------------------------------------------------

upload_sensor(df) => Responsável pela planilha de sensores
upload_historico(df) => Responsável pela planilha de historicos
upload_ambiente(df) => Responsável pela planilha de ambientes

'''


#----------------------------------------------------------------------------------------------------------
def upload_sensor(df):
    colunas_nescessarias = ["sensor", "mac_address", 'latitude', "unidade_medida", "longitude", "status"]

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


#----------------------------------------------------------------------------------------------------------
def upload_historico(df):
    colunas_nescessarias = ["sensor", "ambiente" ,"valor" , "timestamp"]

    # Verifica se todas as colunas estão presentes no dataframe
    if not all(coluna in df.columns for coluna in colunas_nescessarias):
        return Response({"Erro": "A planilha não contém as colunas necessárias."}, status=status.HTTP_400_BAD_REQUEST)

    for index, row, in df.iterrows():
        #Pegando os campos na planilha
        sensor_id = row['sensor']
        ambiente_id = row['ambiente']

        #É preciso obter a instancia do objeto para fazer a relação entre os modelos
        try:
            sensor_obj = Sensor.objects.get(id=sensor_id)
        except Sensor.DoesNotExist:
            return Response({"Erro": f"Sensor com id {sensor_id} não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        try:
            ambiente_obj = Ambiente.objects.get(id=ambiente_id)
        except Ambiente.DoesNotExist:
            return Response({"Erro": f"Ambiente com id {ambiente_id} não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        dados = Historico(
            sensor=sensor_obj,
            ambiente=ambiente_obj,
            valor=row['valor'],
            timestamp = row['timestamp'],
            )
        dados.save()


#----------------------------------------------------------------------------------------------------------
def upload_ambiente(df):
    colunas_nescessarias = ["sig","descricao","ni", "responsavel"]

    # Verifica se todas as colunas estão presentes no dataframe
    if not all(coluna in df.columns for coluna in colunas_nescessarias):
        return Response({"Erro": "A planilha não contém as colunas necessárias."}, status=status.HTTP_400_BAD_REQUEST)
    
    for index, row, in df.iterrows():
        dados = Ambiente(
            sig=row['sig'],
            descricao=row['descricao'],
            ni=row['ni'],
            responsavel = row['responsavel'],
            )
        dados.save()