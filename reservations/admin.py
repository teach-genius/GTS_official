from django.contrib import admin
from orientation.models import MessageSupportTechnique

@admin.register(MessageSupportTechnique)
class MessageSupportTechniqueAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'email', 'subject', 'cree_a')
    search_fields = ('firstName', 'lastName', 'email', 'subject')
    list_filter = ('cree_a',)