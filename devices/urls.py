from django.urls import path
from .views import device_register
from .views import device_graphic
from .views import device_statistics
from .views import device_update
from .views import device_delete
from .views import device_conf
from .views import device_messages


urlpatterns = [
    path('deviceregister/<int:pk>/', device_register, name='deviceregister'),
    path('devicegraphic/<int:pk>/', device_graphic, name='devicegraphic'),
    path('devicestatistics/<int:pk>/', device_statistics, name='devicestatistics'),
    path('deviceupdate/<int:pk>/', device_update, name='deviceupdate'),
    path('devicedelete/<int:pk>/', device_delete, name='devicedelete'),
    path('deviceconf/<int:pk>/', device_conf, name='deviceconf'),
    path('devicemessages/<int:pk>/', device_messages, name='devicemessages'),
]
