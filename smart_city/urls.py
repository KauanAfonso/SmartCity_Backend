from django.urls import path
from .views import carregar_planilhas

urlpatterns = [
    path("upload_planilha/", carregar_planilhas, name="upload_planilha")  # A URL associada à view carregar_planilhas
]
