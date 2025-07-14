import uuid
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.urls import reverse
from ecoles.models import Ecole, PreInscription, ProgrammeScolaire
from logements.models import Logement,DemandeVisite
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from ecoles.models import Ecole ,TypeEcole,EcoleImage # ajuste selon ton app
import requests


User = get_user_model()

def dashboard_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        context = {
            'total_utilisateurs': User.objects.filter(is_superuser=True).count(),
            'etablissements': Ecole.objects.count(),
            'visites': DemandeVisite.objects.filter(status='En attente').count(),
            'preinscription': PreInscription.objects.filter(statut='En attente').count(),
            'logement': Logement.objects.count()
        }
        return render(request, 'dashboard/index.html', context)
    else:
        return HttpResponse("note autorized page note existe")




def logements_view(request):
    return render(request,"dashboard/logements.html")

def parametre_view(request):
    return render(request,"dashboard/parametre.html")


def supprimer_pre_view(request):
    if request.method == 'POST':
        identifiant = request.POST.get('Supprimer_pre')
        if identifiant:
            pre_ins = get_object_or_404(PreInscription, identifiant=identifiant)
            pre_ins.delete()
        return redirect(request.META.get('HTTP_REFERER', 'preinscription'))


def approuver_pre_view(request):
    if request.method == 'POST':
        identifiant = request.POST.get('approuver_pre')
        if identifiant:
            pre_ins = get_object_or_404(PreInscription, identifiant=identifiant)
            pre_ins.statut = "Approuvée"
            pre_ins.support_tech_msg = "Nous avons le plaisir de vous informer que votre demande de préinscription a été approuvée."
            pre_ins.save()
        return redirect(request.META.get('HTTP_REFERER', 'preinscription'))

def preinscription_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        context = {
            'preinscription': PreInscription.objects.all()
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

def rejet_demande_view(request):
    if request.method == "POST":
        id_demande = request.POST.get('id_preinscription_demande')
        motif = request.POST.get('motif', '').strip()  # correction : .strip() au lieu de .trip()

        if motif:
            pre = get_object_or_404(PreInscription, identifiant=id_demande)
            pre.support_tech_msg = motif
            pre.statut = "Refusée"
            pre.save()
        
        # Redirection dans tous les cas (avec ou sans motif)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('preinscription')))
    
    return HttpResponseRedirect(reverse('preinscription'))





def modifi_school(request):
    if request.method == "POST":
        ecole_id = request.POST.get("ecole_id")
        nom = request.POST.get("nom")
        type_id = request.POST.get("type")
        description = request.POST.get("description")
        site_web = request.POST.get("site")
        notation = request.POST.get("note")
        email = request.POST.get("email")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        telephone = request.POST.get("telephone")
        ville = request.POST.get("ville")
        admission = request.POST.get("admission")

        # Images
        first_img = request.POST.get("image_url_1")
        second_img = request.POST.get("image_url_2")
        three_img = request.POST.get("image_url_3")

        try:
            ecole = get_object_or_404(Ecole, id=ecole_id)

            type_ecole = TypeEcole.objects.get(nom=type_id) if type_id else None

            # Mettre à jour les champs
            ecole.nom = nom
            ecole.type_ecole = type_ecole
            ecole.description = description
            ecole.site_web = site_web
            ecole.notation = notation
            ecole.email = email
            ecole.latitude = latitude
            ecole.longitude = longitude
            ecole.telephone = telephone
            ecole.ville = ville
            ecole.admission = admission
            ecole.emplacement = ville
            ecole.save()

            # Si de nouvelles images sont fournies, les ajouter
            for image_url in [first_img, second_img, three_img]:
                if image_url:
                    EcoleImage.objects.create(
                        ecole=ecole,
                        image_url=image_url
                    )

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('etablissement')))

        except Exception as e:
            print(f"Erreur lors de la modification : {e}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('etablissement')))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('etablissement')))


def ajoute_school(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        type_id = request.POST.get("type")
        description = request.POST.get("description")
        site_web = request.POST.get("site")
        notation = request.POST.get("note")
        email = request.POST.get("email")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        telephone = request.POST.get("telephone")
        ville = request.POST.get("ville")
        admission = request.POST.get("admission")

        # Images
        first_img = request.POST.get("image_url_1")
        second_img = request.POST.get("image_url_2")
        three_img = request.POST.get("image_url_3")

        try:
            type_ecole = TypeEcole.objects.get(nom=type_id) if type_id else None

            # 1. Créer l'école
            ecole = Ecole.objects.create(
                nom=nom,
                type_ecole=type_ecole,
                description=description,
                site_web=site_web,
                notation=notation,
                email=email,
                latitude=latitude,
                longitude=longitude,
                emplacement=ville,
                telephone=telephone,
                ville=ville,
                admission=admission,
            )

            # 2. Ajouter les images associées
            for image_url in [first_img, second_img, three_img]:
                if image_url:  # vérifie si l'image est fournie
                    EcoleImage.objects.create(
                        ecole=ecole,
                        image_url=image_url
                    )

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('etablissement')))

        except Exception as e:
            print(f"Erreur : {e}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('etablissement')))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('etablissement')))


def modifi_school(request):
    if request.method == "POST":
        ecole_id = request.POST.get("ecole_id")
        nom = request.POST.get("nom")
        type_id = request.POST.get("type")
        description = request.POST.get("description")
        site_web = request.POST.get("site")
        notation = request.POST.get("note")
        email = request.POST.get("email")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        telephone = request.POST.get("telephone")
        ville = request.POST.get("ville")
        admission = request.POST.get("admission")

        # Images
        first_img = request.POST.get("image_url_1")
        second_img = request.POST.get("image_url_2")
        three_img = request.POST.get("image_url_3")

        try:
            ecole = get_object_or_404(Ecole, identifiant=ecole_id)

            type_ecole = TypeEcole.objects.get(nom=type_id) if type_id else None

            # Mettre à jour les champs
            ecole.nom = nom
            ecole.type_ecole = type_ecole
            ecole.description = description
            ecole.site_web = site_web
            ecole.notation = notation
            ecole.email = email
            ecole.latitude = latitude
            ecole.longitude = longitude
            ecole.telephone = telephone
            ecole.ville = ville
            ecole.admission = admission
            ecole.emplacement = ville
            ecole.save()

            # Si de nouvelles images sont fournies, les ajouter
            for image_url in [first_img, second_img, three_img]:
                if image_url:
                    EcoleImage.objects.create(
                        ecole=ecole,
                        image_url=image_url
                    )

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('etablissement')))

        except Exception as e:
            print(f"Erreur lors de la modification : {e}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('etablissement')))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('etablissement')))



def confirmer_view(request):
    if request.method == "POST":
        id_demande = request.POST.get("iDdemande")
        # Récupère la demande ou renvoie une 404 si elle n'existe pas
        demande = get_object_or_404(DemandeVisite, identifiant=id_demande)

        # Change le statut
        demande.status = "Confirmée"
        demande.save()

        # Redirection ou message de confirmation
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('reservation')))
    else:
        return HttpResponse("Méthode non autorisée", status=405)
    
def annuler_view(request):
    if request.method == "POST":
        id_demande = request.POST.get("iDdemande")

        # Récupère la demande ou renvoie une 404 si elle n'existe pas
        demande = get_object_or_404(DemandeVisite, identifiant=id_demande)

        # Supprime la demande
        demande.delete()

        # Redirection avec confirmation
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('reservation')))
    else:
        return HttpResponse("Méthode non autorisée", status=405)
        

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
    all_tpes = TypeEcole.objects.all()
    formations = ProgrammeScolaire.objects.all()

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
    paginator = Paginator(etablissements, 52)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    url = "https://countriesnow.space/api/v0.1/countries/cities"
    payload = {"country": "Morocco"}
    try:
        response = requests.post(url, json=payload)
        data = response.json()

        if data.get("error") is False:
            villes = data.get("data", [])
        else:
            villes = []

    except Exception as e:
        print("Erreur:", e)
        villes = []

    context = {
        'page_obj': page_obj,
        'total': paginator.count,
        'query': query,
        'ville': ville,
        'type': type_ecole,
        'all_tpes':all_tpes,
        "villes": villes,
        "formations": formations,
    }
    return render(request, "dashboard/etablissement.html", context)




from django.views.decorators.http import require_POST
@require_POST
def ajouter_formation(request):
    id_ecole = request.POST.get('id_ecole')
    nom = request.POST.get('nom_formation')
    degre = request.POST.get('degre_formation')
    description = request.POST.get('description_formation')
    duree = request.POST.get('duree_formation')
    prix = request.POST.get('prix_formation')

    ecole = get_object_or_404(Ecole, identifiant=id_ecole)

    ProgrammeScolaire.objects.create(
        identifiant_ecole=ecole,
        type_de_degre=degre,
        nom=nom,
        description=description,
        duree=duree,
        cout_max=prix,
        devise="MAD",  # Assuming the currency is MAD, adjust as necessary
        identifiant=uuid.uuid4()
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('etablissement')))






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