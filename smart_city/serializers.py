from rest_framework import serializers
from .models import Sensor, Ambiente, Historico
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
    
    def create(self, validated_data):
        password = validated_data.pop('password') #retirando a senha 
        user = User.objects.create(**validated_data)  # Pegando os dados e validando 
        user.set_password(password) #Hashando a senha
        user.save() #salvando
        return user
#-------------------------------------------------Serializer de Sensor--------------------------------------------------------
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

#-------------------------------------------------Serializer de Ambiente--------------------------------------------------------
class AmbienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambiente
        fields = '__all__'

#-------------------------------------------------Serializer de Historico--------------------------------------------------------
class HistoricoSerializer(serializers.ModelSerializer):
    #Realizando o join para obter informações da tabela relacionada
    ambiente_nome = serializers.CharField(source='ambiente.descricao', read_only=True)
    sensor_nome = serializers.CharField(source='sensor.sensor', read_only=True)
    class Meta:
        model = Historico
        fields = ["sensor", "ambiente" ,"valor" , "timestamp", "ambiente_nome", "sensor_nome"]

#-------------------------------------------------Serializer de Login-----------------------------------------------------------
class LoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        data = super().validate(attrs)
 
        data['user'] ={
            'username': self.user.username,
            'email':self.user.email,
        }

        return data