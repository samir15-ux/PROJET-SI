from django.contrib import admin
from django.contrib import admin
from .models import Employe, Service, Conge, Salaire, Contrat, Recrutement, Evaluation, SoldeConge

# Register your models here.

class EmployeAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'prenom', 'date_embauche', 'id_service')
    search_fields = ('nom', 'prenom', 'code')
    list_filter = ('id_service', 'date_embauche')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('description',)

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



class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('employe', 'date', 'note', 'commentaire')
    list_filter = ('date',)
    search_fields = ('employe__nom', 'employe__prenom')

class FavorisAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'url')
    search_fields = ('name',)

# Enregistrement des modèles avec leurs classes admin respectives
admin.site.register(Employe, EmployeAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Conge, CongeAdmin)
admin.site.register(Salaire, SalaireAdmin)
admin.site.register(Contrat, ContratAdmin)
admin.site.register(Recrutement, RecrutementAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
@admin.register(SoldeConge)
class SoldeCongeAdmin(admin.ModelAdmin):
    list_display = ('employe', 'solde_annuel', 'solde_maladie')
    search_fields = ('employe__nom', 'employe__prenom')



