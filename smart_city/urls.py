from django.urls import path
from .views import upload_sheets , handle_sensor

urlpatterns = [
    path("upload/", view=upload_sheets),  # A URL associada à view carregar_planilhas
    path("sensores/<int:pk>", view=handle_sensor)
]
