# your_app_name/admin.py
from django.contrib import admin
from .models import LogementType, LogementAmenity, Logement, LogementImage, DemandeVisite, FavorisLogement


class LogementImageInline(admin.TabularInline):
    model = LogementImage
    extra = 1  
    fields = ('image_url', 'description', 'order') 

@admin.register(LogementType)
class LogementTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(LogementAmenity)
class LogementAmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class')
    search_fields = ('name',)

@admin.register(Logement)
class LogementAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'logement_type', 'city', 'price_per_month', 
        'num_bedrooms', 'num_bathrooms', 'rating', 'created_at'
    )
    list_filter = ('logement_type', 'city', 'amenities', 'num_bedrooms', 'num_bathrooms')
    search_fields = ('title', 'description', 'address', 'city')
    filter_horizontal = ('amenities',) 
    inlines = [LogementImageInline] 

@admin.register(DemandeVisite)
class DemandeVisiteAdmin(admin.ModelAdmin):
    list_display = ('logement', 'user', 'requested_date', 'status', 'created_at')
    list_filter = ('status', 'requested_date', 'logement__city', 'logement__logement_type')
    search_fields = ('logement__title', 'user__username', 'user__email', 'message')
    raw_id_fields = ('user', 'logement') 

@admin.register(FavorisLogement)
class FavorisLogementAdmin(admin.ModelAdmin):
    list_display = ('logement', 'user', 'created_at')
    list_filter = ('created_at', 'logement__city', 'logement__logement_type')
    search_fields = ('logement__title', 'user__username', 'user__email')
    raw_id_fields = ('user', 'logement') 