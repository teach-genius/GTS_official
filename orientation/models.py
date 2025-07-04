from django.db import models
from django.conf import settings
import uuid
# Create your models here.


class MessageSupportTechnique(models.Model):
    identifiant = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    est_lu = models.BooleanField(default=False)
    cree_a = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"message du {self.cree_a}"

    class Meta:
        verbose_name = "MessageSupport"
        verbose_name_plural = "MessageSupports"
        ordering = ['-cree_a']