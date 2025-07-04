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
from django.urls import path
from .views import confirm_email, connexion_view,deconnexion_view
from django.conf import settings
from django.conf.urls.static import static
from .views import registre_view
from connexion import views

urlpatterns = [
    path('',connexion_view,name='connexion'),
    path('deconnexion/',deconnexion_view,name='deconnexion'),
    path('registre/',registre_view,name='registre'),
      # Confirmation de l'email
    path('confirmation/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),

    # Renvoi du lien d'activation
    path('renvoyer-lien/', views.resend_activation_link, name='resend_activation_link'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
