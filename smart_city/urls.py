from django.urls import path
from .views import upload_sheets , handle_sensor , logar, handle_ambiente, handle_historico, registrar,exportar_sensores, exportar_hostorico, exportar_ambientes

urlpatterns = [
    #upload
    path("upload/", view=upload_sheets),

    #Sensores
    path('sensores/', handle_sensor),      
    path("sensores/<int:pk>", view=handle_sensor),

    #Ambientes
    path("ambientes/", view=handle_ambiente),
    path("ambientes/<int:pk>", view=handle_ambiente),

    #Historicos
    path("historicos/", view=handle_historico),
    path("historicos/<int:pk>", view=handle_historico),

    #Login
    path("login/", view=logar),
    path("registrar/", view=registrar),

    #Exportar
    path("exportar/sensores/", view=exportar_sensores),
    path("exportar/ambientes/", view=exportar_ambientes),
    path("exportar/historico/", view=exportar_hostorico),
]
