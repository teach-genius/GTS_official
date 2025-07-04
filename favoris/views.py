from django.shortcuts import render
from logements.models import FavorisLogement
from ecoles.models import FavorisUtilisateur
from connexion.views import get_result



def logement_view(request):
    user = request.user
    mes_logements = FavorisLogement.objects.filter(user=user).order_by('-created_at')
    mes_ecoles = FavorisUtilisateur.objects.filter(id_de_l_utilisateur=user).order_by('-cree_a')
    context = {
        'active_tab': 'logements',
        'mes_logements': mes_logements, 
        'total_logements':mes_logements.count(),
        'total_ecoles':mes_ecoles.count(),
        'total_favoris':mes_logements.count()+mes_ecoles.count()
    }
    info_plus = get_result(user)
    context["total_d"] = info_plus["total_d"]
    return render(request,'favoris/favoris_logement.html', context)


def ecole_view(request):
    user = request.user
    mes_ecoles = FavorisUtilisateur.objects.filter(id_de_l_utilisateur=user).order_by('-cree_a')
    mes_logements = FavorisLogement.objects.filter(user=user).order_by('-created_at')
    context = {
        'active_tab': 'ecoles',
        'mes_ecoles': mes_ecoles, 
        'total_ecoles':mes_ecoles.count(),
        'total_logements':mes_logements.count(),
        'total_favoris':mes_logements.count()+mes_ecoles.count(),
    }
    info_plus = get_result(user)
    context["total_d"] = info_plus["total_d"]
    return render(request,'favoris/favoris_ecole.html', context)