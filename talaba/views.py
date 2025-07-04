from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from ecoles.models import PreInscription
from logements.models import DemandeVisite
from orientation.models import MessageSupportTechnique
from django.contrib import messages
from logements.models import DemandeVisite
from ecoles.models import PreInscription
from connexion.views import get_result

def home_view(request):
    if request.user.is_authenticated:
        user = request.user  # tu définis user ici
        
        mes_preinscriptions = PreInscription.objects.filter(id_de_l_utilisateur=user.id).order_by('cree_a')
        mes_logements = DemandeVisite.objects.filter(user=user).order_by('-created_at')
        
        context = {
            'total_preinscriptions': mes_preinscriptions.count(),
            'total_demande': mes_logements.count(),
            'total_d': mes_preinscriptions.count() + mes_logements.count()
        }
    else:
        context = {
            'total_preinscriptions': 0,
            'total_demande': 0,
            'total_d': 0
        }

    return render(request, 'index.html', context)



def contact_view(request):
    if request.method == "POST":
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        MessageSupportTechnique.objects.create(
            firstName=firstName,
            lastName=lastName,
            email=email,
            subject=subject,
            message=message
        )
        

        messages.success(request, "Votre formulaire a été soumis avec succès.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('contact')))

    else:
        context = get_result(request.user)
        return render(request,"contact.html",context)
