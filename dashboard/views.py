from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from ecoles.models import Ecole, PreInscription
from logements.models import Logement,DemandeVisite
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from ecoles.models import Ecole  # ajuste selon ton app


User = get_user_model()

def dashboard_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        context = {
            'total_utilisateurs': User.objects.filter(is_superuser=True).count(),
            'etablissements': Ecole.objects.count(),
            'visites': DemandeVisite.objects.count(),
            'preinscription': PreInscription.objects.count(),
            'logement': Logement.objects.count()
        }
        return render(request, 'dashboard/index.html', context)
    else:
        return HttpResponse("note autorized page note existe")




def logements_view(request):
    return render(request,"dashboard/logements.html")

def parametre_view(request):
    return render(request,"dashboard/parametre.html")


def preinscription_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        context = {
            'preinscription': PreInscription.objects
        }
        return render(request,"dashboard/preinscription.html",context)
    else:
        return HttpResponse("note autorized page note existe")
    

def reservation_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        context = {
            'dVisite': DemandeVisite.objects.all()
        }
    return render(request,"dashboard/reservation.html",context)



def statistique_view(request):
    return render(request,"dashboard/statistique.html")



def etablissement_view(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login')  # ou HttpResponseForbidden()

    # Récupération des filtres
    query = request.GET.get('q', '')
    ville = request.GET.get('ville', '')
    type_ecole = request.GET.get('type', '')

    # Filtrage des écoles
    etablissements = Ecole.objects.all()

    if query:
        etablissements = etablissements.filter(
            Q(nom__icontains=query) |
            Q(ville__icontains=query) |
            Q(description__icontains=query)
        )
    if ville:
        etablissements = etablissements.filter(ville__iexact=ville)
    if type_ecole:
        etablissements = etablissements.filter(type_ecole__nom__iexact=type_ecole)

    # Pagination (8 établissements par page)
    paginator = Paginator(etablissements, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total': paginator.count,
        'query': query,
        'ville': ville,
        'type': type_ecole,
    }
    return render(request, "dashboard/etablissement.html", context)


def notifications_view(request):
    return render(request,"dashboard/notifications.html")

def utilisateurs_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        # Fetch all users who are NOT superusers
        users = User.objects.filter(is_superuser=False).order_by('username') # Added ordering for better presentation
        context = {
            "users": users # This 'users' variable will be available as 'user_list' in your template
        }
        return render(request, "dashboard/utilisateurs.html", context)