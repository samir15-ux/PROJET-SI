from django.urls import include, path
from . import views
from .views import connexion, inscription,gestion_tables

urlpatterns = [

    path('login/', connexion, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', inscription, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.index, name='index'),
    
    path ( 'gestion_tables' ,gestion_tables, name='gestion_tables'),
    #  chemins similaires pour employe
    path('employes/', views.gestion_employes, name='gestion_employes'),
    path('employes/ajouter/', views.ajouter_employe, name='ajouter_employe'),
    path('employes/modifier/<int:pk>/', views.modifier_employe, name='modifier_employe'),
    path('employes/supprimer/<int:pk>/', views.supprimer_employe, name='supprimer_employe'),
    #  chemins similaires pour Service
    path('services/', views.gestion_services, name='gestion_services'),
    path('services/ajouter/', views.ajouter_service, name='ajouter_service'),
    path('services/<int:pk>/modifier/', views.modifier_service, name='modifier_service'),
    path('services/<int:pk>/supprimer/', views.supprimer_service, name='supprimer_service'),
    #  chemins similaires pour conge
    path('conges/', views.gestion_conges, name='gestion_conges'),
    path('conges/ajouter/', views.ajouter_conge, name='ajouter_conge'),
    path('conges/<int:pk>/modifier/', views.modifier_conge, name='modifier_conge'),
    path('conges/<int:pk>/supprimer/', views.supprimer_conge, name='supprimer_conge'),

    path('soldes/', views.solde_conge_list, name='solde_conge_list'),  # Liste des soldes de congés
    path('soldes/<int:employe_id>/update/', views.solde_conge_update, name='solde_conge_update'),  # Modifier un solde
    
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
    

      # Gestion_personnel
    path('personnel/', views.Gestion_personnel, name='Gestion_personnel'),
    path('personnel/<int:pk>/', views.fiche_employe, name='fiche_employe'),
    path('personnel/<int:pk>/ajouter_evaluation/', views.ajouter_evaluation, name='ajouter_evaluation'),

]
