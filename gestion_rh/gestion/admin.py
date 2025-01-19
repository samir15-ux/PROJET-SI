from django.contrib import admin
from django.contrib import admin
from .models import Employe, Conges, Salaire, Contrat, Recrutement, Candidature, Evaluation, SoldeConge

class EmployeAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'prenom', 'date_embauche')
    search_fields = ('nom', 'prenom', 'code')
    list_filter = ( 'date_embauche','departement', 'poste')

class CongesAdmin(admin.ModelAdmin):
    list_display = ('employe', 'type_conge', 'date_debut', 'date_fin')
    list_filter = ('type_conge', 'date_debut')
    search_fields = ('employe__nom', 'employe__prenom')

class SalaireAdmin(admin.ModelAdmin):
    list_display = ('employe', 'salaire_base', 'primes', 'heures_supplementaires')
   

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

class SoldeCongeAdmin(admin.ModelAdmin):
     list_display = (
        'employe', 
        'solde_restant_annuel', 
        'solde_restant_maladie', 
        'solde_restant_maternite' 
        
    )
    

admin.site.register(Employe, EmployeAdmin)
admin.site.register(Conges, CongesAdmin)
admin.site.register(Salaire, SalaireAdmin)
admin.site.register(Contrat, ContratAdmin)
admin.site.register(Recrutement, RecrutementAdmin)
admin.site.register(Candidature, CandidatureAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(SoldeConge, SoldeCongeAdmin)




