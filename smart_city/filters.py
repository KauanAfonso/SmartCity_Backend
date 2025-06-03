from .models import Sensor, Ambiente, Historico
from .serializers import SensorSerializer, LoginSerializer ,AmbienteSerializer, HistoricoSerializer
import django_filters

class SensorFiltro(django_filters.FilterSet):
    sensor = django_filters.CharFilter(field_name='sensor', lookup_expr='exact')
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')
    class Meta:
        model = Sensor
        fields  = ['sensor', 'status']

class HistoricoFilter(django_filters.FilterSet):
    # Exemplo de filtro por data exata
    timestamp = django_filters.DateTimeFilter(field_name='timestamp')

    class Meta:
        model = Historico
        fields = ['timestamp']

class AmbienteFiltro(django_filters.FilterSet):
    sig = django_filters.NumberFilter(field_name="sig", lookup_expr='exact')
    class Meta:
        model = Ambiente
        fields = ["sig"]