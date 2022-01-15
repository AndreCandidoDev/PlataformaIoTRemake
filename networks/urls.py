from django.urls import path
from .views import network_register
from .views import network_dashboard
from .views import network_delete
from .views import device_network_register
from .views import device_network_update
from .views import device_network_delete
from .views import device_network_configuration
from .views import device_network_serial

urlpatterns = [
    path('network_register/<int:pk>/', network_register, name='network_register'),
    path('network_dashboard/<slug:identificador>/', network_dashboard, name='network_dashboard'),
    path('network_delete/<slug:identificador>/', network_delete, name='network_delete'),
    path('device_network_register/<slug:identificador>/', device_network_register, name='device_network_register'),
    path('device_network_update/<slug:dispositivo_serial>/', device_network_update, name='device_network_update'),
    path('device_network_delete/<slug:dispositivo_serial>/', device_network_delete, name='device_network_delete'),
    path('device_network_configuration/<slug:dispositivo_serial>/', device_network_configuration, name='device_network_configuration'),
    path('device_network_serial/<slug:dispositivo_serial>/', device_network_serial, name='device_network_serial')
]