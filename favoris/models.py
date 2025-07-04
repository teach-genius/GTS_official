# from django.db import models
# from django.conf import settings
# import uuid

# class Notification(models.Model):
#     type_notification = models.CharField(max_length=100) 
#     titre = models.CharField(max_length=255)
#     message = models.TextField()
#     identifiant_de_reference = models.UUIDField(null=True, blank=True) 
#     type_de_reference = models.CharField(max_length=100, null=True, blank=True) 
#     est_lu = models.BooleanField(default=False)
#     cree_a = models.DateTimeField(auto_now_add=True)
#     identifiant_utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications_recues', null=True, blank=True) # User who this notification is for
#     identifiant = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

#     def __str__(self):
#         return f"Notification pour {self.identifiant_utilisateur.username if self.identifiant_utilisateur else 'N/A'} : {self.titre} ({self.type_notification})"

#     class Meta:
#         verbose_name = "Notification"
#         verbose_name_plural = "Notifications"
#         ordering = ['-cree_a']



