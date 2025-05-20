from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    tipo = models.CharField(
        max_length=2, 
        choices=(("A", "Administrador"), ("UC", "Usuário Comum"))
    )

    def __str__(self):
        return self.username 

class Sensor(models.Model):
    sensor = models.CharField(max_length=255)
    mac_address = models.CharField(max_length=255) 
    unidade_med = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.BooleanField()

    def __str__(self):
        return self.sensor  

class Ambiente(models.Model):
    sig = models.IntegerField()
    descricao = models.CharField(max_length=255)
    ni = models.CharField(max_length=255)
    responsavel = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao  

class Historico(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    ambiente = models.ForeignKey(Ambiente, on_delete=models.CASCADE)
    valor = models.FloatField()
    timestamp = models.IntegerField() 

    def __str__(self):
        return f"Sensor: {self.sensor}, Ambiente: {self.ambiente}" 
    



#24240125