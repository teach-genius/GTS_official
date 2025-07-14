"""
URL configuration for talaba project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from .views import home_view,contact_view,gts_pro_view,conf_view,utilisation_view,rembourse_view,cook_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin_talaba_dash/', admin.site.urls),
    path('',home_view,name='home'),
    path('ecoles/', include(('ecoles.urls','ecoles'),namespace='ecoles')),
    path('logements/', include(('logements.urls', 'logements'), namespace='logements')),
    path('contact/', contact_view,name='contact'),
    path('orientation/', include(('orientation.urls', 'orientation'), namespace='orientation')),
    path('connexion/',include('connexion.urls'),name='connexion'),
    path('deconnexion/',include('connexion.urls'),name='deconnexion'),
    path('dashboard/',include('dashboard.urls'),name='dashboard'),
    path('reservations/',include('reservations.urls'),name='reservations'),
    path('favoris/',include('favoris.urls'),name='favoris'),
    path('gts_pro/',gts_pro_view,name='gts_pro'),
    path('conf/',conf_view,name="conf"),
    path('utilisation/',utilisation_view,name="utilisation"),
    path('rembourse/',rembourse_view,name="rembourse"),
    path('cook/',cook_view,name="cook"),
    
]
# 12345678
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
