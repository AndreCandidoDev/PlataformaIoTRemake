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
from .views import profile_register
from .views import profile_update
from .views import plano_change
from .views import plano_update
from .views import plano_upgrade

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
    path('profileregister/', profile_register, name='profileregister'),
    path('profileupdate/<int:pk>/', profile_update, name='profileupdate'),
    path('planochange/<int:pk>/', plano_change, name='planochange'),
    path('planoupdate/<int:pk>/', plano_update, name='planoupdate'),
    path('planoupgrade/<int:pk>/', plano_upgrade, name='planoupgrade'),
]
