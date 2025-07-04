from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.db import IntegrityError
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from ecoles.models import PreInscription
from logements.models import DemandeVisite


User = get_user_model()

def get_result(user):
    if user.is_authenticated:
        mes_preinscriptions = PreInscription.objects.filter(id_de_l_utilisateur=user.id).order_by('cree_a')
        mes_logements = DemandeVisite.objects.filter(user=user).order_by('-created_at')
        
        context = {
            'total_d': mes_preinscriptions.count() + mes_logements.count()
        }
    else:
        context = {
            'total_d': 0
        }
    return context


def connexion_view(request):
    if request.user.is_authenticated:
        messages.info(request, "Vous êtes déjà connecté.")
        return redirect(reverse('home'))

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Connexion réussie ! Bienvenue !")
                return redirect(reverse('home'))
            else:
                messages.warning(request, "Votre compte n'est pas encore activé. Veuillez vérifier votre email.")
                return redirect('resend_activation_link')
        else:
            messages.error(request, "Email ou mot de passe invalide.")
            return render(request, 'connexion/index.html', {'email': email})  # <-- AJOUTÉ ICI

    return render(request, 'connexion/index.html')  # <-- Pas dans le else, mais hors du bloc POST


def deconnexion_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect(reverse('home'))


def registre_view(request):
    if request.method == 'POST':
        # Récupération des données
        first_name = request.POST.get('firstName', '').strip()
        last_name = request.POST.get('lastName', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirmPassword', '').strip()

        errors = {}

        # Validation
        if not first_name:
            errors['firstName'] = "Le prénom est requis."
        if not last_name:
            errors['lastName'] = "Le nom est requis."
        if not email:
            errors['email'] = "L'email est requis."
        elif '@' not in email or '.' not in email:
            errors['email'] = "Veuillez entrer une adresse email valide."
        else:
            try:
                existing_user = User.objects.get(email=email)
                if existing_user.is_active:
                    errors['email'] = "Cette adresse email est déjà utilisée."
                else:
                    messages.info(request, "Compte non activé. Vérifiez vos emails")
                    return redirect('resend_activation_link')  # Tu dois créer cette vue
            except User.DoesNotExist:
                pass  # Email non utilisé → OK

        if not password:
            errors['password'] = "Le mot de passe est requis."
        elif len(password) < 8:
            errors['password'] = "Le mot de passe doit contenir au moins 8 caractères."
        if password != confirm_password:
            errors['confirmPassword'] = "Les mots de passe ne correspondent pas."

        if errors:
            for field, error_message in errors.items():
                messages.error(request, f"{field}: {error_message}")
            return render(request, 'registre/index.html', {
                'errors': errors,
                'firstName': first_name,
                'lastName': last_name,
                'email': email,
            })

        try:
            # Création du compte inactif
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=False
            )

            # Générer le lien de confirmation
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = request.build_absolute_uri(
                reverse('confirm_email', kwargs={'uidb64': uid, 'token': token})
            )

            # Envoyer l'email
            subject = "Confirmez votre adresse e-mail"
            message = render_to_string('email/activation_email.html', {
                'user': user,
                'activation_link': activation_link
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            messages.success(request, "Un email de confirmation a été envoyé.")
            return redirect('connexion')
        except IntegrityError:
            messages.error(request, "Une erreur est survenue lors de la création du compte.")
        except Exception as e:
            messages.error(request, f"Erreur : {e}")

    return render(request, 'registre/index.html')




def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Votre email a été confirmé. Vous pouvez maintenant vous connecter.")
            return redirect('connexion')
        else:
            messages.error(request, "Le lien de confirmation est invalide ou expiré.")
    except Exception:
        messages.error(request, "Lien de confirmation invalide.")

    return redirect('connexion')



def resend_activation_link(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                activation_link = request.build_absolute_uri(
                    reverse('confirm_email', kwargs={'uidb64': uid, 'token': token})
                )
                message = render_to_string('email/activation_email.html', {
                    'user': user,
                    'activation_link': activation_link
                })
                send_mail("Confirmation de votre compte", message, settings.DEFAULT_FROM_EMAIL, [email])
                messages.success(request, "Un nouveau lien de confirmation a été envoyé.")
            else:
                messages.info(request, "Ce compte est déjà actif.")
        except User.DoesNotExist:
            messages.error(request, "Aucun compte trouvé avec cet email.")
        return redirect('connexion')
    return render(request, 'email/resend_activation.html')
