from django.urls import path
from .views import device_register
from .views import device_statistics
from .views import device_update
from .views import device_delete
from .views import device_conf
from .views import device_messages
from .views import device_serial
from .views import device_csv_generator
from .views import device_pdf_generator


urlpatterns = [
    path('deviceregister/<int:pk>/', device_register, name='deviceregister'),
    path('devicestatistics/<dispositivo_serial>/', device_statistics, name='devicestatistics'),
    path('deviceupdate/<slug:dispositivo_serial>/', device_update, name='deviceupdate'),
    path('devicedelete/<slug:dispositivo_serial>/', device_delete, name='devicedelete'),
    path('deviceconf/<slug:dispositivo_serial>/', device_conf, name='deviceconf'),
    path('devicemessages/<slug:dispositivo_serial>/', device_messages, name='devicemessages'),
    path('deviceserial/<slug:dispositivo_serial>/', device_serial, name='deviceserial'),
    path('devicecsv/<slug:dispositivo_serial>/', device_csv_generator, name='devicecsv'),
    path('devicepdf/<slug:dispositivo_serial>/', device_pdf_generator, name='devicepdf')
]
