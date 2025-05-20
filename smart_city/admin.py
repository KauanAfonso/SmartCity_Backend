from django.contrib import admin
from .models import Usuario, Sensor, Ambiente, Historico
# Register your models here.
admin.site.register((Usuario, Sensor, Ambiente, Historico))