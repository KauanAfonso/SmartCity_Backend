from django.urls import path
from .views import upload_sheets , handle_sensor , logar, handle_ambiente

urlpatterns = [
    path("upload/", view=upload_sheets),  # A URL associada à view carregar_planilhas
    path('sensores/', handle_sensor),      
    path("sensores/<int:pk>", view=handle_sensor),
    path("ambientes/", view=handle_ambiente),
    path("ambientes/<int:pk>", view=handle_ambiente),
    path("login/", view=logar)
]
