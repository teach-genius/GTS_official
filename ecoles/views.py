# ecoles/views.py

from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Q, OuterRef, Exists, Value, Case, When
from django.db.models.fields import BooleanField
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect 
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import decimal
from jsonschema import ValidationError

from logements.models import DemandeVisite
# Assurez-vous d'importer tous vos modèles nécessaires depuis votre fichier models.py
from .models import Ecole, TypeEcole, EcoleImage, FavorisUtilisateur, ProgrammeScolaire, PreInscription
from django.shortcuts import  redirect
from django.contrib import messages
from .models import PreInscription, Ecole, ProgrammeScolaire
from datetime import datetime # Pour convertir la date de naissance
from django.contrib import messages
from connexion.views import get_result




class EcoleListView(ListView):
    """
    Vue basée sur une classe pour afficher une liste d'écoles,
    avec des fonctionnalités de recherche, de filtrage et
    l'indication si une école est en favoris pour l'utilisateur connecté.
    """
    model = Ecole
    context_object_name = 'ecoles'
    template_name = 'ecoles/index.html'
    paginate_by = 8 # Nombre d'écoles par page

    def get_queryset(self):
        """
        Construit et retourne le queryset des écoles.
        Inclut la logique pour la recherche, le filtrage et l'annotation
        du statut "favoris" pour l'utilisateur authentifié.
        """
        # Récupérer le queryset de base et optimiser les requêtes
        queryset = super().get_queryset().select_related('type_ecole').prefetch_related(
            Prefetch('images', queryset=EcoleImage.objects.order_by('order') if hasattr(EcoleImage, 'order') else EcoleImage.objects.all()),
            'programmes_scolaires', 
        )

        # Logique pour annoter si l'école est en favoris pour l'utilisateur actuel
        if self.request.user.is_authenticated:
            user = self.request.user
            print(f"DEBUG: Utilisateur authentifié dans EcoleListView: {user.username} (ID: {user.id})")
            favorited_school_uuids = set(
                FavorisUtilisateur.objects.filter(id_de_l_utilisateur=user)
                .values_list('identifiant_ecole', flat=True) # Récupère directement l'UUID de l'école
            )
            print(f"DEBUG: UUIDs des écoles en favoris pour l'utilisateur {user.username}: {favorited_school_uuids}")

            # Annotes le queryset principal avec un champ booléen 'is_favorited_by_user'.
            # On utilise 'Ecole.identifiant' pour la comparaison, car c'est l'UUID.
            queryset = queryset.annotate(
                is_favorited_by_user=Case(
                    When(identifiant__in=favorited_school_uuids, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            )
        else:
            # Si l'utilisateur n'est pas authentifié, aucune école n'est "en favoris"
            queryset = queryset.annotate(is_favorited_by_user=Value(False, output_field=BooleanField()))
            print("DEBUG: Utilisateur non authentifié. 'is_favorited_by_user' mis à False pour toutes les écoles.")

        # Récupération des paramètres de recherche et de filtrage de l'URL
        search_query = self.request.GET.get('search', '').strip()
        city_filter = self.request.GET.get('city', '').strip()
        type_filter_name = self.request.GET.get('type', '').strip()

        # Application des filtres
        if search_query:
            queryset = queryset.filter(
                Q(nom__icontains=search_query) |      # Recherche par nom de l'école
                Q(emplacement__icontains=search_query) |  # Recherche par emplacement
                Q(description__icontains=search_query) |  # Recherche par description
                Q(type_ecole__nom__icontains=search_query) # Recherche par nom du type d'école
            ).distinct()

        if city_filter:
            queryset = queryset.filter(ville__icontains=city_filter)

        if type_filter_name:
            queryset = queryset.filter(type_ecole__nom__iexact=type_filter_name)
        
        #print(f"DEBUG: Nombre d'écoles dans le queryset après filtres: {queryset.count()}")
        return queryset.order_by('nom') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Valeurs par défaut si l’utilisateur n’est pas connecté
        total_preinscriptions = 0
        total_demandes = 0

        # Si l’utilisateur est connecté, calculer les totaux
        if self.request.user.is_authenticated:
            user = self.request.user
            total_preinscriptions = PreInscription.objects.filter(id_de_l_utilisateur=user).count()
            total_demandes = DemandeVisite.objects.filter(user=user).count()
        
        # Calculer le total
        context['total_d'] = total_preinscriptions + total_demandes
        context['all_types'] = TypeEcole.objects.all().order_by('nom')
        context['all_cities'] = Ecole.objects.values_list('ville', flat=True).filter(ville__isnull=False).distinct().order_by('ville')
        context['current_search'] = self.request.GET.get('search', '')
        context['current_city'] = self.request.GET.get('city', '')
        context['current_type'] = self.request.GET.get('type', '')
        context['total_ecoles'] = self.get_queryset().count() 
        ecoles_processed = []
        for ecole in context['ecoles']: 
            is_fav = getattr(ecole, 'is_favorited_by_user', False)
            ecole.is_favorite = is_fav 
            ecoles_processed.append(ecole)
           # print(f"DEBUG: Traitement de l'école '{ecole.nom}' (ID: {ecole.id}, Identifiant UUID: {ecole.identifiant}). is_favorited_by_user (annotation): {ecole.is_favorited_by_user}, is_favorite (pour le template): {ecole.is_favorite}")
        context['ecoles'] = ecoles_processed 
        
        return context


@login_required
@require_POST
def toggle_favoris(request):
    if(request.POST.get('EcoleId')):
        ecole_identifiant = request.POST.get('EcoleId')
    
    ecole = get_object_or_404(Ecole, identifiant=ecole_identifiant)
    favoris_entry, created = FavorisUtilisateur.objects.get_or_create(
        id_de_l_utilisateur=request.user,
        identifiant_ecole=ecole
    )
    if created:
        messages.info(request, "Ecole ajouté aux favoris")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('ecoles:ecoles')))
    else:
        favoris_entry.delete()
        messages.info(request, "Ecole supprimé des favoris")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('ecoles:ecoles')))

@login_required
@require_POST
def toggle_favoris_voir(request):
    if(request.POST.get('Ecole_Id_f')):
        ecole_identifiant = request.POST.get('Ecole_Id_f')
    
    ecole = get_object_or_404(Ecole, identifiant=ecole_identifiant)
    favoris_entry, created = FavorisUtilisateur.objects.get_or_create(
        id_de_l_utilisateur=request.user,
        identifiant_ecole=ecole
    )
    if created:
        messages.info(request, "Ecole ajouté aux favoris")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('ecoles:ecoles')))
    else:
        favoris_entry.delete()
        messages.info(request, "Ecole supprimé des favoris ")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('ecoles:ecoles')))
    


@require_POST
@login_required
def faire_demande_now(request):
    # Récupération des données du formulaire
    civilite = request.POST.get('gender')
    prenom = request.POST.get('prenom')
    nom = request.POST.get('nom')
    email = request.POST.get('email')
    telephone = request.POST.get('telephone')
    birthday_str = request.POST.get('birthday')
    errors = {}
    # Verification for empty fields
    if not civilite:
        errors['gender'] = 'La civilité est obligatoire.'

    # Using .strip() to account for fields that might contain only whitespace
    if not prenom or not prenom.strip():
        errors['prenom'] = 'Le prénom est obligatoire.'

    if not nom or not nom.strip():
        errors['nom'] = 'Le nom est obligatoire.'

    if not email:
        errors['email'] = "L'adresse email est obligatoire."

    if not telephone:
        errors['telephone'] = 'Le numéro de téléphone est obligatoire.'

    if not birthday_str:
        errors['birthday'] = 'La date de naissance est obligatoire.'
    
    if errors:
        messages.warning(request,"operation avortée veuillez remplire les champs du formulaire au complet")
        return redirect('ecoles:ecoles')
    else:
        date_de_naissance = None
        if birthday_str:
            try:
                date_de_naissance = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            except ValueError:
                print(f"Erreur: Format de date invalide pour la date de naissance: {birthday_str}")
                return HttpResponse("Erreur: Format de date de naissance invalide.", status=400)

        cni = request.POST.get('cni')
        pays = request.POST.get('pays')
        ville = request.POST.get('ville')

        current_education_ville = request.POST.get('current_education_ville')
        current_education_etablissement = request.POST.get('current_education_etablissement')

        annee_bac = request.POST.get('annee_bac')
        serie_bac = request.POST.get('serie_bac')
        
        # --- CORRECTION ICI POUR MOYENNE BAC ---
        moyenne_bac_str = request.POST.get('moyenne_bac')
        moyenne_bac_cleaned = None
        if moyenne_bac_str:
            try:
                # Convertir en Decimal et arrondir
                moyenne_bac_cleaned = decimal.Decimal(moyenne_bac_str).quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_HALF_UP)
            except decimal.InvalidOperation:
                print(f"Erreur: La moyenne du bac '{moyenne_bac_str}' n'est pas un nombre valide.")
                return HttpResponse("Erreur: La moyenne du bac doit être un nombre valide.", status=400)
        
        print(f"DEBUG: 'moyenne_bac_cleaned' après traitement: {moyenne_bac_cleaned} (Type: {type(moyenne_bac_cleaned)})")
        # --- FIN DE CORRECTION MOYENNE BAC ---

        programme_identifiant_str = request.POST.get('formation_id')
        print(f"DEBUG: id recuperé pour la formation {programme_identifiant_str}")
        programme = None
        ecole = None

        try:
            programme = ProgrammeScolaire.objects.get(identifiant=programme_identifiant_str)
            ecole_uuid_du_programme = programme.identifiant_ecole.identifiant
            ecole = Ecole.objects.get(identifiant=ecole_uuid_du_programme)
        except ProgrammeScolaire.DoesNotExist:
            print(f"Erreur: Programme Scolaire avec l'identifiant '{programme_identifiant_str}' introuvable.")
            return HttpResponse("Erreur: Formation sélectionnée introuvable.", status=400)
        except Ecole.DoesNotExist:
            print(f"Erreur: École avec l'identifiant '{ecole_uuid_du_programme}' introuvable.")
            return HttpResponse("Erreur: École associée à la formation introuvable.", status=400)
        except Exception as e:
            print(f"Erreur inattendue lors de la récupération du programme ou de l'école : {e}")
            return HttpResponse(f"Erreur serveur: {e}", status=500)

        # Traitement des fichiers téléchargés
        photo_file = request.FILES.get('photo_upload_input')
        cv_file = request.FILES.get('cv_upload_input')
        releve_notes_file = request.FILES.get('releve_notes_upload_input')
        bac_diploma_file = request.FILES.get('bac_diploma_upload_input')
        cni_copy_file = request.FILES.get('cni_copy_upload_input')
        lettre_motivation_file = request.FILES.get('lettre_motivation_input')
        recommandation_file = request.FILES.get('recommandation_load_input')

        if photo_file and bac_diploma_file and releve_notes_file:
            message = request.POST.get('message')

            # Création de l'objet PreInscription
            pre_inscription = PreInscription(
                id_de_l_utilisateur=request.user,
                identifiant_ecole=ecole,
                programme_id=programme,
                nom_etudiant=f"{prenom} {nom}",
                email_de_l_etudiant=email,
                telephone_etudiant=telephone,
                date_de_naissance=date_de_naissance,
                ville=ville,
                pays=pays,
                passeport_cin=cni,
                civilite=civilite,
                annee_d_obtention_du_bac=annee_bac,
                bac_series=serie_bac,
                moyenne_bac_regionale=moyenne_bac_cleaned, # <-- PAS DE float() ICI ! Passez l'objet Decimal ou None.
                message=message,
                ville_actuelle = current_education_ville, 
                ecole_actuelle = current_education_etablissement, 
            )
            
            # Assigner les fichiers directement aux champs FileField/ImageField du modèle
            if photo_file:
                pre_inscription.photo = photo_file
            if cv_file:
                pre_inscription.cv = cv_file
            if releve_notes_file:
                pre_inscription.releve_notes = releve_notes_file
            if bac_diploma_file:
                pre_inscription.bac_diploma = bac_diploma_file
            if cni_copy_file:
                pre_inscription.cni_copy = cni_copy_file
            if lettre_motivation_file:
                pre_inscription.lettre_motivation = lettre_motivation_file
            if recommandation_file:
                pre_inscription.recommandation = recommandation_file

            try:
                pre_inscription.full_clean() # Valide les données
                pre_inscription.save()       # Enregistre l'objet ET les fichiers sur le disque

                # Maintenant que l'objet est sauvegardé et les fichiers sont sur le disque,
                # leurs URLs sont disponibles via l'attribut .url
                documents_telecharges_meta = {}
                if pre_inscription.photo:
                    documents_telecharges_meta['photo_url'] = pre_inscription.photo.url
                if pre_inscription.cv:
                    documents_telecharges_meta['cv_url'] = pre_inscription.cv.url
                if pre_inscription.releve_notes:
                    documents_telecharges_meta['releve_notes_url'] = pre_inscription.releve_notes.url
                if pre_inscription.bac_diploma:
                    documents_telecharges_meta['bac_diploma_url'] = pre_inscription.bac_diploma.url
                if pre_inscription.cni_copy:
                    documents_telecharges_meta['cni_copy_url'] = pre_inscription.cni_copy.url
                if pre_inscription.lettre_motivation:
                    documents_telecharges_meta['lettre_motivation_url'] = pre_inscription.lettre_motivation.url
                if pre_inscription.recommandation:
                    documents_telecharges_meta['recommandation_url'] = pre_inscription.recommandation.url

                # Mettre à jour le champ documents_telecharger avec les URLs
                pre_inscription.documents_telecharger = documents_telecharges_meta
                pre_inscription.save(update_fields=['documents_telecharger']) # Sauvegarder uniquement ce champ

                print("Pré-inscription et fichiers enregistrés avec succès.")
                print(f"URLs des documents sauvegardés: {documents_telecharges_meta}")

                return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('ecoles:ecoles')))
            except ValidationError as e:
                print(f"Erreur de validation lors de la sauvegarde: {e.message_dict}")
                # Afficher un message plus spécifique à l'utilisateur
                error_messages = [f"{k}: {', '.join(v)}" for k, v in e.message_dict.items()]
                return HttpResponse(f"Erreur de validation: {'; '.join(error_messages)}", status=400)
            except Exception as e:
                print(f"Erreur inattendue lors de la sauvegarde de la pré-inscription: {e}")
                return HttpResponse(f"Erreur lors de l'enregistrement de votre demande : {e}", status=500)
        else:
            messages.warning("operation avortée veuillez remplir les documents obligatoires")
            return redirect('ecoles:ecoles')