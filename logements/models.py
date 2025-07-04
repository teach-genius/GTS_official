from django.db import models
from django.conf import settings
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

# --- Modèles de base pour le Logement ---

class LogementType(models.Model):
    """
    Représente les différents types de logement (Appartement, Villa, Studio, Maison).
    Cela permet une gestion plus flexible des types.
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="Nom du type de logement")

    class Meta:
        verbose_name = "Type de Logement"
        verbose_name_plural = "Types de Logements"
        ordering = ['name']

    def __str__(self):
        return self.name

class LogementAmenity(models.Model):
    """
    Représente un équipement ou une caractéristique disponible dans un logement
    (ex: Wifi, Piscine, Climatisation, Parking).
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom de l'équipement/caractéristique")
    icon_class = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        help_text="Classe Font Awesome de l'icône (ex: fas fa-wifi)",
        verbose_name="Icône"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description de l'équipement")

    class Meta:
        verbose_name = "Équipement de Logement"
        verbose_name_plural = "Équipements de Logements"
        ordering = ['name']

    def __str__(self):
        return self.name

class Logement(models.Model):
    """
    Représente une annonce de logement.
    """
    CITIES = [
        ('Casablanca', 'Casablanca'),
        ('Rabat', 'Rabat'),
        ('Marrakech', 'Marrakech'),
        ('Tanger', 'Tanger'),
        ('Fès', 'Fès'),
        ('Agadir', 'Agadir'),
    ]

    # Informations de base
    title = models.CharField(max_length=255, verbose_name="Titre de l'annonce")
    description = models.TextField(verbose_name="Description détaillée du logement")
    
    # Localisation
    city = models.CharField(max_length=100, choices=CITIES, verbose_name="Ville")
    address = models.CharField(max_length=255, verbose_name="Adresse complète")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Longitude")

    # Détails du logement
    logement_type = models.ForeignKey(LogementType, on_delete=models.SET_NULL, null=True, related_name='logements', verbose_name="Type de logement")
    surface_area = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Surface (m²)", 
                                       help_text="Surface en mètres carrés", validators=[MinValueValidator(1.0)])
    num_bedrooms = models.IntegerField(verbose_name="Nombre de chambres", default=1, 
                                       validators=[MinValueValidator(0)])
    num_bathrooms = models.IntegerField(verbose_name="Nombre de salles de bain", default=1, 
                                        validators=[MinValueValidator(0)])
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix par mois (DH)",
                                          validators=[MinValueValidator(0.0)])
    currency = models.CharField(max_length=10, default='DH', verbose_name="Devise")
    
    # Notation
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, 
                                 validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], 
                                 verbose_name="Note moyenne")

    # Horodatage et identifiant unique
    identifiant = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="Identifiant unique")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    # Relations ManyToMany
    amenities = models.ManyToManyField(LogementAmenity, related_name='logements', blank=True, verbose_name="Équipements")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Logement"
        verbose_name_plural = "Logements"
        ordering = ['-created_at']

class LogementImage(models.Model):
    """
    Modèle pour stocker les images associées à un logement.
    Un logement peut avoir plusieurs images.
    """
    logement = models.ForeignKey(Logement, on_delete=models.CASCADE, related_name='images', verbose_name="Logement")
    image_url = models.URLField(max_length=2000, verbose_name="URL de l'image")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Description de l'image")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return f"Image pour {self.logement.title} ({self.order})"

    class Meta:
        verbose_name = "Image de Logement"
        verbose_name_plural = "Images de Logements"
        ordering = ['order'] 


class DemandeVisite(models.Model):
    """
    Modèle pour gérer les demandes de visite de logement des utilisateurs.
    """
    STATUS_CHOICES = [
        ('En attente', 'En attente'),
        ('Confirmée', 'Confirmée'),
        ('Annulée', 'Annulée'),
        ('Terminée', 'Terminée'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='demandes_visite', verbose_name="Utilisateur")
    logement = models.ForeignKey(Logement, on_delete=models.CASCADE, related_name='demandes_visite', verbose_name="Logement")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Numéro de téléphone")
    email = models.EmailField(blank=True, null=True, verbose_name="Adresse e-mail")
    requested_date = models.DateField(verbose_name="Date souhaitée de la visite")
    requested_time = models.CharField(max_length=50, blank=True, null=True, verbose_name="Heure souhaitée (ex: 'Matin', 'Après-midi', '14h00')")
    message = models.TextField(blank=True, null=True, verbose_name="Message de l'utilisateur")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='En attente', verbose_name="Statut de la demande")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de la demande")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    def __str__(self):
        return f"Demande de visite pour {self.logement.title} par {self.user.username} le {self.requested_date}"

    class Meta:
        verbose_name = "Demande de Visite"
        verbose_name_plural = "Demandes de Visite"
        ordering = ['-created_at']

class FavorisLogement(models.Model):
    """
    Modèle pour gérer les logements favoris d'un utilisateur.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favoris_logements', verbose_name="Utilisateur")
    logement = models.ForeignKey(Logement, on_delete=models.CASCADE, related_name='favoris', verbose_name="Logement")
    identifiant = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="Identifiant unique du favori")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout aux favoris")

    class Meta:
        verbose_name = "Favori Logement"
        verbose_name_plural = "Favoris Logements"
        unique_together = ('user', 'logement') 
        ordering = ['-created_at']

    def __str__(self):
        return f"Favori de {self.user.username} pour {self.logement.title}"