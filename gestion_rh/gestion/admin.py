from django.contrib import admin
from django.contrib import admin
from .models import Employe, Conge, Salaire, Contrat, Recrutement, Candidature, Evaluation, SoldeConge

# Register your models here.

class EmployeAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'prenom', 'date_embauche')
    search_fields = ('nom', 'prenom', 'code')
    list_filter = ( 'date_embauche','departement', 'poste')

class CongeAdmin(admin.ModelAdmin):
    list_display = ('employe', 'type_conge', 'date_debut', 'date_fin')
    list_filter = ('type_conge', 'date_debut')
    search_fields = ('employe__nom', 'employe__prenom')

class SalaireAdmin(admin.ModelAdmin):
    list_display = ('employe', 'mois', 'salaire_base', 'primes', 'salaire_final')
    list_filter = ('mois',)
    search_fields = ('employe__nom', 'employe__prenom')

class ContratAdmin(admin.ModelAdmin):
    list_display = ('employe', 'type_contrat', 'date_debut', 'date_fin', 'salaire_mensuel')
    list_filter = ('type_contrat', 'date_debut')
    search_fields = ('employe__nom', 'employe__prenom')

class RecrutementAdmin(admin.ModelAdmin):
    list_display = ('poste', 'date_publication', 'date_limite')
    search_fields = ('poste',)

class CandidatureAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'etat')
    search_fields = ('prenom', 'nom', 'etat', 'email')

class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('employe', 'date', 'note', 'commentaire')
    list_filter = ('date',)
    search_fields = ('employe__nom', 'employe__prenom')

class FavorisAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'url')
    search_fields = ('name',)

# Enregistrement des modèles avec leurs classes admin respectives
admin.site.register(Employe, EmployeAdmin)
admin.site.register(Conge, CongeAdmin)
admin.site.register(Salaire, SalaireAdmin)
admin.site.register(Contrat, ContratAdmin)
admin.site.register(Recrutement, RecrutementAdmin)
admin.site.register(Candidature, CandidatureAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
@admin.register(SoldeConge)
class SoldeCongeAdmin(admin.ModelAdmin):
    list_display = ('employe', 'solde_annuel', 'solde_maladie')
    search_fields = ('employe__nom', 'employe__prenom')



