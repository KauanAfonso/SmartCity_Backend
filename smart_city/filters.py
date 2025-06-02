from .models import Sensor, Ambiente, Historico
from .serializers import SensorSerializer, LoginSerializer ,AmbienteSerializer, HistoricoSerializer
import django_filters

class SensorFiltro(django_filters.FilterSet):
    sensor = django_filters.CharFilter(field_name='sensor', lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status', lookup_expr='icontains')
    class Meta:
        model = Sensor
        fields  = ['sensor', 'status']


# class HistoricoSerializer(django_filters.FilterSet):
#     data = django_filters.DateTimeFilter(field_name='data', lookup_expr='icontais')
#     class Meta:
#         model = Historico
#         fields = ["timestamp"]

class AmbienteFiltro(django_filters.FilterSet):
    sig = django_filters.NumberFilter(field_name="sig", lookup_expr='exact')
    class Meta:
        model = Ambiente
        fields = ["sig"]