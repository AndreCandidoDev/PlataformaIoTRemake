"""plataforma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from accounts import urls as accounts_urls
from devices import urls as devices_urls
from devicesapi import urls as devicesapi_urls
# from devicesapi.urls import router
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('usecases/', views.usecases, name='usecases'),
    path('pricing/', views.pricing, name='pricing'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('support/', views.support, name='support'),
    path('datapolitics/', views.datapolitics, name='datapolitics'),
    path('examples/', views.examples, name='examples'),
    path('admin/', admin.site.urls),
    path('accounts/', include(accounts_urls)),
    path('devices/', include(devices_urls)),
    path('api/v1/', include(devicesapi_urls)),
    # path('api/v1/', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
