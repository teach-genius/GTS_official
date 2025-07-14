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
from .views import (
    ajouter_formation,
    dashboard_view,
    parametre_view,
    logements_view,
    reservation_view,
    statistique_view,
    preinscription_view,
    etablissement_view,
    notifications_view,
    utilisateurs_view,
    confirmer_view,
    annuler_view,
    rejet_demande_view,
    supprimer_pre_view,
    approuver_pre_view,
    ajoute_school,
    modifi_school
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',dashboard_view,name='dashboard'),
    path('parametre/',parametre_view,name="parametre"),
    path('statistique/',statistique_view,name='statistique'),
    path('preinscription/',preinscription_view,name='preinscription'),
    path('logements_dash/',logements_view,name='logements_dash'),
    path('reservation/',reservation_view,name='reservation'),
    path('etablissement/',etablissement_view,name="etablissement"),
    path('notifications/',notifications_view,name="notifications"),
    path('utilisateurs/',utilisateurs_view,name="utilisateurs"),
    path('confirmer/',confirmer_view,name="confirmer"),
    path('annuler/',annuler_view,name="annuler"),
    path('rejet_demande/',rejet_demande_view,name='rejet_demande'),
    path('Supprimer_pre/',supprimer_pre_view,name='Supprimer_pre'),
    path('approuver_pre/',approuver_pre_view,name='approuver_pre'),
    path('add_school/',ajoute_school,name='ajoute_school'),
    path('modifi_school/',modifi_school,name='modifi_school'),
    path('ajouter_formation_ecole/',ajouter_formation,name='ajouter_formation_ecole')   

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
