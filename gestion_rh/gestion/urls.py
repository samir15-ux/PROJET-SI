from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import connexion, employe_dashboard, inscription,gestion_tables, postuler

urlpatterns = [

    path('login/', connexion, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', inscription, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.index, name='index'),
    path('postuler/', postuler, name='postuler'),
    path('gestion_candidatures/', views.Gestion_candidature, name='Gestion_candidature'),
    path('candidature/<int:candidature_id>/update/', views.update_candidature, name='update_candidature'),
    path ( 'gestion_tables' ,gestion_tables, name='gestion_tables'),
    path('employe/dashboard/', employe_dashboard, name='employe_dashboard'),
    path('modifier-informations/', views.modifier_informations, name='modifier_informations'),

    #  chemins similaires pour employe
    path('employes/', views.gestion_employes, name='gestion_employes'),
    path('employes/ajouter/', views.ajouter_employe, name='ajouter_employe'),
    path('employes/modifier/<int:pk>/', views.modifier_employe, name='modifier_employe'),
    path('employes/supprimer/<int:pk>/', views.supprimer_employe, name='supprimer_employe'),

    #  chemins similaires pour conge
    path('conges/', views.gestion_conges, name='gestion_conges'),
    path('conges/ajouter/', views.ajouter_conge, name='ajouter_conge'),
    path('conges/<int:pk>/modifier/', views.modifier_conge, name='modifier_conge'),
    path('conges/<int:pk>/supprimer/', views.supprimer_conge, name='supprimer_conge'),
    path('demande-conge/', views.demande_conge, name='demande_conge'),
    path('consulter-conges/', views.consulter_conges, name='consulter_conges'),
    path('changer-statut/<int:conge_id>/', views.changer_statut, name='changer_statut'),

  
    
    #  chemins similaires pour salaire
    path('salaires/', views.gestion_salaires, name='gestion_salaires'),
    path('salaires/ajouter/', views.ajouter_salaire, name='ajouter_salaire'),
    path('salaires/<int:pk>/modifier/', views.modifier_salaire, name='modifier_salaire'), 
    path('salaires/<int:pk>/supprimer/', views.supprimer_salaire, name='supprimer_salaire'),

    #  chemins similaires pour contrat
    path('contrats/', views.gestion_contrats, name='gestion_contrats'),
    path('contrats/ajouter/', views.ajouter_contrat, name='ajouter_contrat'),
    path('contrats/<int:pk>/modifier/', views.modifier_contrat, name='modifier_contrat'),
    path('contrats/<int:pk>/supprimer/', views.supprimer_contrat, name='supprimer_contrat'),
    
    #  chemins similaires pour recrutements
    path('recrutements/', views.gestion_recrutements, name='gestion_recrutements'),
    path('recrutements/ajouter/', views.ajouter_recrutement, name='ajouter_recrutement'),
    path('recrutements/<int:pk>/modifier/', views.modifier_recrutement, name='modifier_recrutement'),
    path('recrutements/<int:pk>/supprimer/', views.supprimer_recrutement, name='supprimer_recrutement'),

      # Gestion_personnel
    path('personnel/', views.Gestion_personnel, name='Gestion_personnel'),
    path('personnel/<int:pk>/', views.fiche_employe, name='fiche_employe'),
    path('personnel/<int:pk>/ajouter_evaluation/', views.ajouter_evaluation, name='ajouter_evaluation'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
