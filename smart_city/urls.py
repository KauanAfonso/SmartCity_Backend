from django.urls import path
from .views import upload_sheets

urlpatterns = [
    path("upload/", view=upload_sheets)  # A URL associada à view carregar_planilhas
]
