# from django.db import models
# import uuid
# from django.contrib.auth.models import User

# class UtilisateurAdmin(models.Model):
#     # Assuming ID de l'utilisateur maps to Django's built-in User model
#     id_de_l_utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='admin_profile')
#     identifiant = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     role = models.CharField(max_length=100)
#     autorisations = models.JSONField(null=True, blank=True)
#     cree_a = models.DateTimeField(auto_now_add=True)
#     mis_a_jour_a = models.DateTimeField(auto_now=True)
#     peut_gerer_les_ecoles = models.BooleanField(default=False)
#     peut_gerer_les_logements = models.BooleanField(default=False)
#     peut_gerer_les_inscriptions = models.BooleanField(default=False)
#     peut_gerer_les_reservations = models.BooleanField(default=False)
#     peut_gerer_les_utilisateurs = models.BooleanField(default=False)
#     peut_voir_analytics = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Admin: {self.id_de_l_utilisateur.username} - {self.role}"

#     class Meta:
#         verbose_name = "Utilisateur Admin"
#         verbose_name_plural = "Utilisateurs Admin"
#         ordering = ['cree_a']

# class NotificationAdmin(models.Model):
#     type_notification = models.CharField(max_length=100) # Renommé 'taper' en 'type_notification'
#     titre = models.CharField(max_length=255)
#     message = models.TextField()
#     identifiant_de_reference = models.UUIDField(null=True, blank=True) # ID of the related object (e.g., a PreInscription ID)
#     type_de_reference = models.CharField(max_length=100, null=True, blank=True) # e.g., 'PreInscription', 'Logement'
#     identifiant_utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_notifications_recues', null=True, blank=True) # User who this notification is for (if specific)
#     identifiant = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     est_lu = models.BooleanField(default=False)
#     cree_a = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Notification: {self.titre} ({self.type_notification})"

#     class Meta:
#         verbose_name = "Notification Admin"
#         verbose_name_plural = "Notifications Admin"
#         ordering = ['-cree_a']