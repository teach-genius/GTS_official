from django.contrib import admin
from .models import Ecole, EcoleImage, ProgrammeScolaire, PreInscription, FavorisUtilisateur, TypeEcole # Ajout de TypeEcole

class EcoleImageInline(admin.TabularInline):
    model = EcoleImage
    extra = 1

@admin.register(Ecole)
class EcoleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'get_type_ecole_display', 'ville', 'telephone', 'email', 'notation', 'cree_a') # Modifié
    search_fields = ('nom', 'ville', 'type_ecole__nom') # Modifié
    list_filter = ('type_ecole', 'ville')
    inlines = [EcoleImageInline]

    def get_type_ecole_display(self, obj):
        return obj.type_ecole.nom if obj.type_ecole else "N/A"
    get_type_ecole_display.short_description = "Type d'école"


@admin.register(EcoleImage)
class EcoleImageAdmin(admin.ModelAdmin):
    list_display = ('ecole', 'image_url', 'cree_a')
    list_filter = ('ecole',)
    search_fields = ('ecole__nom',)


@admin.register(TypeEcole) # Nouvel enregistrement pour TypeEcole
class TypeEcoleAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
    list_filter = ('nom',)


@admin.register(ProgrammeScolaire)
class ProgrammeScolaireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'identifiant_ecole', 'type_de_degre', 'duree', 'cout_min', 'cout_max')
    search_fields = ('nom', 'identifiant_ecole__nom', 'type_de_degre')
    list_filter = ('type_de_degre', 'identifiant_ecole')

@admin.register(PreInscription)
class PreInscriptionAdmin(admin.ModelAdmin):
    list_display = ('nom_etudiant', 'email_de_l_etudiant', 'identifiant_ecole', 'programme_id', 'statut', 'cree_a')
    list_filter = ('statut', 'identifiant_ecole', 'programme_id', 'ville')
    search_fields = ('nom_etudiant', 'email_de_l_etudiant', 'identifiant_ecole__nom', 'passeport_cin')
    readonly_fields = ('cree_a',)

@admin.register(FavorisUtilisateur)
class FavorisUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('id_de_l_utilisateur', 'identifiant_ecole', 'cree_a')
    list_filter = ('identifiant_ecole', 'id_de_l_utilisateur')
    search_fields = ('id_de_l_utilisateur__username', 'identifiant_ecole__nom')