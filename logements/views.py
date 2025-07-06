from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef, Prefetch, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from ecoles.models import PreInscription


from .models import DemandeVisite, FavorisLogement, Logement, LogementImage, LogementType


class ListeLogementsView(ListView):
    model = Logement
    template_name = 'logements/index.html'
    context_object_name = 'logements'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        
        queryset = queryset.select_related('logement_type').prefetch_related(
            Prefetch('images', queryset=LogementImage.objects.order_by('order')),
            'amenities'
        )

        if self.request.user.is_authenticated:
            favorited_subquery = FavorisLogement.objects.filter(
                user=self.request.user,
                logement=OuterRef('pk')
            )
            queryset = queryset.annotate(
                is_favorited_by_user=Exists(favorited_subquery)
            )

        search_keyword = self.request.GET.get('q', '').strip()
        if search_keyword:
            queryset = queryset.filter(
                Q(title__icontains=search_keyword) |
                Q(description__icontains=search_keyword) |
                Q(city__icontains=search_keyword) |
                Q(address__icontains=search_keyword) |
                Q(amenities__name__icontains=search_keyword)
            ).distinct()

        filter_city = self.request.GET.get('city', '').strip()
        if filter_city:
            queryset = queryset.filter(city__iexact=filter_city)

        filter_type = self.request.GET.get('type', '').strip()
        if filter_type:
            queryset = queryset.filter(logement_type__name__iexact=filter_type)

        return queryset.order_by('-created_at')

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


        context['selected_city'] = self.request.GET.get('city', '')
        context['selected_type'] = self.request.GET.get('type', '')
        context['search_keyword'] = self.request.GET.get('q', '')

        context['cities_available'] = Logement.objects.values_list('city', flat=True).distinct().order_by('city')
        context['types_available'] = LogementType.objects.values_list('name', flat=True).distinct().order_by('name')

        context['total_logements_count'] = self.get_queryset().count()

        logements_processed = []
        for logement in context['logements']: 
            logement.is_favorite = getattr(logement, 'is_favorited_by_user', False)
            logements_processed.append(logement)
        context['logements'] = logements_processed

        return context


@login_required
@require_POST
def toggle_favoris(request):
    logement_identifiant = request.POST.get('logementId')
    logement = get_object_or_404(Logement, identifiant=logement_identifiant)
    favoris_entry, created = FavorisLogement.objects.get_or_create(
        user=request.user,
        logement=logement
    )
    if created:
        messages.info(request," logement Ajouté aux favoris")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('logements:logements')))
    else:
        favoris_entry.delete()
        messages.info(request," logement retiré des favoris ")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('logements:logements')))

    



@login_required
@require_POST
def reserver_visite(request):
    logement_identifiant = request.POST.get('logementIdReserver')
    preferred_date_str = request.POST.get('preferredDate')
    preferred_time = request.POST.get('preferredTime')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    message = request.POST.get('message', '')

    # Vérifie si tous les champs obligatoires sont présents
    if not all([logement_identifiant, preferred_date_str, preferred_time, phone, email]):
        messages.warning(request, "Veuillez remplir tous les champs.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('logements:logements')))

    # Vérifie si une demande existe déjà pour le même utilisateur et logement
    if DemandeVisite.objects.filter(user=request.user, logement__identifiant=logement_identifiant).exists():
        messages.warning(request, "Vous avez déjà soumis une demande pour ce logement.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('logements:logements')))

    # Récupère le logement
    logement = get_object_or_404(Logement, identifiant=logement_identifiant)

    # Convertit la date
    try:
        requested_date = datetime.strptime(preferred_date_str, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, "Date invalide.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('logements:logements')))

    # Crée la demande
    demande = DemandeVisite.objects.create(
        user=request.user,
        logement=logement,
        requested_date=requested_date,
        requested_time=preferred_time,
        phone=phone,
        email=email,
        message=message,
        status='En attente'
    )

    messages.success(request, "Votre demande de visite a été soumise avec succès.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('logements:logements')))
