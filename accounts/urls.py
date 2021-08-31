from django.urls import path
from .views import register
from .views import login
from .views import logout
from .views import dashboard
from .views import activate
from .views import forgotpassword
from .views import resetpassword_validate
from .views import resetpassword
from .views import token
from .views import apidoc
from .views import device_register
from .views import device_graphic
from .views import device_statistics
from .views import device_update
from .views import device_delete
from .views import device_conf
from .views import device_messages

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('forgotpassword/', forgotpassword, name='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>/', resetpassword_validate, name='resetpassword_validate'),
    path('resetpassword/', resetpassword, name='resetpassword'),
    path('token/', token, name='token'),
    path('apidoc/', apidoc, name='apidoc'),
    path('deviceregister/<int:pk>/', device_register, name='deviceregister'),
    path('devicegraphic/<int:pk>/', device_graphic, name='devicegraphic'),
    path('devicestatistics/<int:pk>/', device_statistics, name='devicestatistics'),
    path('deviceupdate/<int:pk>/', device_update, name='deviceupdate'),
    path('devicedelete/<int:pk>/', device_delete, name='devicedelete'),
    path('deviceconf/<int:pk>/', device_conf, name='deviceconf'),
    path('devicemessages/<int:pk>/', device_messages, name='devicemessages')
]