from django.db import models
from django.conf import settings
import uuid

class TypeEcole(models.Model):
    nom = models.CharField(max_length=100, unique=True, help_text="Ex: Université, École d'ingénieurs, École de commerce, Lycée")

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Type d'école"
        verbose_name_plural = "Types d'écoles"
        ordering = ['nom']


class Ecole(models.Model):
    nom = models.CharField(max_length=255)
    type_ecole = models.ForeignKey(TypeEcole, on_delete=models.SET_NULL, null=True, blank=True, related_name='ecoles_par_type')
    description = models.TextField()
    emplacement = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=18, decimal_places=13, null=True, blank=True)
    identifiant = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    longitude = models.DecimalField(max_digits=18, decimal_places=13, null=True, blank=True)
    site_web = models.URLField(max_length=2000, null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    notation = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    admission = models.CharField(max_length=50, null=True, blank=True)
    cree_a = models.DateTimeField(auto_now_add=True)
    mis_a_jour_a = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Ecole"
        verbose_name_plural = "Ecoles"
        ordering = ['-cree_a']

class EcoleImage(models.Model):
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=2000)
    cree_a = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image pour {self.ecole.nom} ({self.image_url})"

    class Meta:
        verbose_name = "Image Ecole"
        verbose_name_plural = "Images Ecoles"
        ordering = ['cree_a']

class ProgrammeScolaire(models.Model):
    identifiant_ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE, to_field='identifiant', related_name='programmes_scolaires')
    nom = models.CharField(max_length=255)
    description = models.TextField()
    duree = models.CharField(max_length=100)
    type_de_degre = models.CharField(max_length=100)
    cout_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    identifiant = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    devise = models.CharField(max_length=10, null=True, blank=True)
    cree_a = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} ({self.identifiant_ecole.identifiant})"

    class Meta:
        verbose_name = "Programme Scolaire"
        verbose_name_plural = "Programmes Scolaires"
        ordering = ['nom']

class PreInscription(models.Model):
    identifiant = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    id_de_l_utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pre_inscriptions')
    identifiant_ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE, to_field='identifiant', related_name='pre_inscriptions')
    programme_id = models.ForeignKey(ProgrammeScolaire, on_delete=models.SET_NULL, null=True, blank=True, to_field='identifiant', related_name='pre_inscriptions')
    nom_etudiant = models.CharField(max_length=255)
    email_de_l_etudiant = models.EmailField()
    telephone_etudiant = models.CharField(max_length=20, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    date_de_naissance = models.DateField(null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    passeport_cin = models.CharField(max_length=50, null=True, blank=True)
    photo_url = models.URLField(max_length=2000, null=True, blank=True)
    master_one_code = models.CharField(max_length=50, null=True, blank=True)
    nom_du_lycee = models.CharField(max_length=255, null=True, blank=True)
    annee_d_obtention_du_bac = models.CharField(max_length=100, null=True, blank=True)
    bac_series = models.CharField(max_length=100, null=True, blank=True)
    moyenne_bac_regionale = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    statut = models.CharField(max_length=50, default='En attente')
    cree_a = models.DateTimeField(auto_now_add=True)
    civilite = models.CharField(max_length=10, null=True, blank=True)
    pays = models.CharField(max_length=100, null=True, blank=True)

    # --- NOUVEAUX CHAMPS POUR LES FICHIERS TÉLÉCHARGÉS ---
    photo = models.ImageField(upload_to='pre_inscriptions/photos/', null=True, blank=True)
    cv = models.FileField(upload_to='pre_inscriptions/cvs/', null=True, blank=True)
    releve_notes = models.FileField(upload_to='pre_inscriptions/releves_notes/', null=True, blank=True)
    bac_diploma = models.FileField(upload_to='pre_inscriptions/bac_diplomas/', null=True, blank=True)
    cni_copy = models.FileField(upload_to='pre_inscriptions/cni_copies/', null=True, blank=True)
    lettre_motivation = models.FileField(upload_to='pre_inscriptions/lettres_motivation/', null=True, blank=True)
    recommandation = models.FileField(upload_to='pre_inscriptions/recommandations/', null=True, blank=True)
    # -----------------------------------------------------

    documents_telecharger = models.JSONField(null=True, blank=True)
    support_tech_msg = models.CharField(max_length=500,null=True,blank=True,default="Votre demande est en attente de traitement. Nous examinerons votre dossier dans les plus brefs délais.")
    ville_actuelle = models.CharField(max_length=100, null=True, blank=True)
    ecole_actuelle = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"Pré-inscription de {self.nom_etudiant} à {self.identifiant_ecole.nom}"

    class Meta:
        verbose_name = "Pré-inscription"
        verbose_name_plural = "Pré-inscriptions"
        ordering = ['-cree_a']

class FavorisUtilisateur(models.Model):
    id_de_l_utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favoris')
    identifiant_ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE, to_field='identifiant', related_name='favoris')
    identifiant = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    cree_a = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Favori Utilisateur"
        verbose_name_plural = "Favoris Utilisateurs"
        unique_together = ('id_de_l_utilisateur', 'identifiant_ecole')
        ordering = ['-cree_a']

    def __str__(self):
        return f"Favori de {self.id_de_l_utilisateur.username} pour {self.identifiant_ecole.nom}"
