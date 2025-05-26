from django.contrib import admin
from .models import Sensor, Ambiente, Historico
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class UsuarioModelAdmin(UserAdmin):
    # adiciona o campo 'email' na tela de criação do usuário no admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email')}),  # precisa ser tupla, então vírgula depois do 'email'
    )
  
  # Primeiro desregistra User padrão (para não duplicar)
admin.site.unregister(User)
# Registra User com o admin customizado
admin.site.register(User, UsuarioModelAdmin)

admin.site.register((Sensor, Ambiente, Historico))