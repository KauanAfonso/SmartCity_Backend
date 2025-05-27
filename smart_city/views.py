import pandas as pd
from rest_framework.decorators import  api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Sensor, Ambiente, Historico
from django.shortcuts import get_object_or_404
from .serializers import SensorSerializer, LoginSerializer ,AmbienteSerializer, HistoricoSerializer, UsuarioSerializer
from .functions import upload_ambiente, upload_historico, upload_sensor
from .filters import SensorFiltro,HistoricoSerializer
#-------------------------------------------------------------------UPLOAD--------------------------------------------------------------------------

@api_view(["POST"])
def upload_sheets(request):
    if request.method == "POST":
        try:
            tipos_permitidos = ['sensor', 'historico', 'ambiente']
            planilha = request.FILES['planilha']
            tipo_planilha = request.data["tipo"]
            if tipo_planilha is None:           
                return Response({"Erro": "Selectione o tipo da planilha."}, status=status.HTTP_400_BAD_REQUEST)
            elif tipo_planilha not in tipos_permitidos:
                return Response({"Erro": "Tipo não permitido."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"Erro": "Aconteceu algum erro para ler a planilha."}, status=status.HTTP_409_CONFLICT)
        
        try:
            df = pd.read_excel(planilha)
            #ao depender do tipo escolido, chamar a função relacionada
            if tipo_planilha == tipos_permitidos[0]:
                upload_sensor(df)

            elif tipo_planilha == tipos_permitidos[1]:
                upload_historico(df)
            
            elif tipo_planilha == tipos_permitidos[2]:
                upload_ambiente(df)

            return Response({"Mensagem": "Dados criados com sucesso"}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"Mensagem": f"Erro: {e}"}, status=status.HTTP_400_BAD_REQUEST)    

#-------------------------------------------------------------------Login--------------------------------------------------------------------------

'''

Login 

'''
@api_view(["POST"])
def logar(request):
    usuario = request.data
    serializer = LoginSerializer(data=usuario)
    if serializer.is_valid():
        return Response({
            "Mensagem": "Logado com sucesso !",
            "Usuário": serializer.validated_data['user'],  # pega os dados do usuário
            "access": serializer.validated_data['access'], 
            "refresh": serializer.validated_data['refresh'],
        }, status=status.HTTP_200_OK)
    return Response({"Mensagem": "Credenciais inválidas"},status=status.HTTP_401_UNAUTHORIZED)  




@api_view(["POST"])
def registrar(request):
    try:
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Mensagem: ": "Usuário registrado com sucesso !"}, status=status.HTTP_201_CREATED)
        return Response({"Mensagem": serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
    except Exception as e:
        return Response({"Mensagem": f"Erro: {e}"}, status=status.HTTP_400_BAD_REQUEST) 
#-------------------------------------------------------------------Sensores--------------------------------------------------------------------------

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
            filtro = SensorFiltro(request.query_params, queryset=Sensor.objects.all())
            if filtro.is_valid():
                dados = filtro.qs
            else:
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
    


#-------------------------------------------------------------------Ambientes--------------------------------------------------------------------------

'''

CRUD para lidar com os ambientes

'''         
@api_view(["GET", "POST", "PUT", "DELETE"])
def handle_ambiente(request, pk=None):
        #Obter um sensor em espécifico ou todos de uma vez !
        if request.method == "GET":
            if pk is not None:
                dados = get_object_or_404(Ambiente, pk=pk)
                serializer = AmbienteSerializer(dados, many=False)
                return Response({"Dados": serializer.data}, status=status.HTTP_200_OK)
            dados = Ambiente.objects.all()
            serializer = AmbienteSerializer(dados, many=True)
            return Response({"Dados": serializer.data}, status=status.HTTP_200_OK)

        #Criar um Ambiente novo e salvar no banco
        elif request.method == "POST":
            dados = request.data
            serializer = AmbienteSerializer(data=dados)
            if serializer.is_valid():
                serializer.save()
                return Response({"Mensagem": "Ambiente registrado com sucesso !"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #Atualizar um Ambiente específico
        elif request.method == "PUT":
            if pk is not None:
                ambiente = get_object_or_404(Ambiente, pk=pk)
                dados = request.data
                serializer = AmbienteSerializer(ambiente, data=dados)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"Mensagem": "Ambiente atualizado com sucesso !"},status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        #Deletar um Ambiente específico
        elif request.method == "DELETE":
            if pk is not None:
                ambiente = get_object_or_404(Ambiente, pk=pk)
                ambiente.delete()
                return Response({"Mensagem": "Ambiente Excluido com sucesso !"},status=status.HTTP_200_OK)
            return Response({"Mensagem": "Erro ao encontrar !"}, status=status.HTTP_400_BAD_REQUEST)        
    



#-------------------------------------------------------------------HISTORICO--------------------------------------------------------------------------
'''

CRUD para lidar com os históricos

'''         
@api_view(["GET", "POST", "PUT", "DELETE"])
def handle_historico(request, pk=None):
        #Obter um sensor em espécifico ou todos de uma vez !
        if request.method == "GET":
            if pk is not None:
                dados = get_object_or_404(Historico, pk=pk)
                serializer = HistoricoSerializer(dados, many=False)
                return Response({"Dados": serializer.data}, status=status.HTTP_200_OK)
            dados = Historico.objects.all()
            serializer = HistoricoSerializer(dados, many=True)
            return Response({"Dados": serializer.data}, status=status.HTTP_200_OK)

        #Criar um histórico novo e salvar no banco
        elif request.method == "POST":
            dados = request.data
            serializer = HistoricoSerializer(data=dados)
            if serializer.is_valid():
                serializer.save()
                return Response({"Mensagem": "histórico registrado com sucesso !"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #Atualizar um histórico específico
        elif request.method == "PUT":
            if pk is not None:
                histórico = get_object_or_404(Historico, pk=pk)
                dados = request.data
                serializer = HistoricoSerializer(histórico, data=dados)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"Mensagem": "histórico atualizado com sucesso !"},status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        #Deletar um histórico específico
        elif request.method == "DELETE":
            if pk is not None:
                histórico = get_object_or_404(Historico, pk=pk)
                histórico.delete()
                return Response({"Mensagem": "histórico Excluido com sucesso !"},status=status.HTTP_200_OK)
            return Response({"Mensagem": "Erro ao encontrar !"}, status=status.HTTP_400_BAD_REQUEST)        
    

