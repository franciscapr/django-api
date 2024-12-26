from rest_framework import viewsets
from rest_framework import filters

class AbstractViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.OrderingFilter]    # Establece el backend de filtrado predeterminado
    ordering_fields = ['updated', 'created']    # Esta lista contiene los campos que pueden usarse como paràmetros de ordenamiento al realizar una solicitud
    ordering = ['-updated']    # Indica el orden en el que se deben enviar muchos objetos como respuesta. En este caso el orden es por los objetos mas recientemente actualizados