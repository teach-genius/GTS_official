from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from logements.models import DemandeVisite, FavorisLogement 
from ecoles.models import PreInscription


def preinscrit_view(request):
    user = request.user
    mes_preinscriptions = PreInscription.objects.filter(id_de_l_utilisateur=user).order_by('cree_a')
    mes_logements = DemandeVisite.objects.filter(user=user).order_by('-created_at')
    context = {
        'active_tab': 'preinscription',
        'total_preinscriptions':mes_preinscriptions.count(),
        'mes_preinscriptions':mes_preinscriptions,
        'total_demande':mes_logements.count(),
        'total_d':mes_preinscriptions.count()+mes_logements.count()
    }
    return  render(request,'reservations/preinscription.html', context)

def logement_view(request):
    user = request.user
    mes_preinscriptions = PreInscription.objects.filter(id_de_l_utilisateur=user).order_by('cree_a')
    mes_logements = DemandeVisite.objects.filter(user=user).order_by('-created_at')
    context = {
        'active_tab': 'logement',
        'mes_logements': mes_logements, 
        'total_demande':mes_logements.count(),
        'total_preinscriptions':mes_preinscriptions.count(),
        'total_d':mes_preinscriptions.count()+mes_logements.count()
    }
    return render(request,'reservations/logement.html', context)


@login_required
def logement_view_favoris(request):
    user = request.user
    logement_favoris = FavorisLogement.objects.filter(user=user).order_by('-created_at')
    context = {
        'active_tab': 'logement',
        'logement_favoris': logement_favoris,
        'total_logement_favoris':logement_favoris.count()
    }
    return render(request, 'reservations/logement.html', context)


