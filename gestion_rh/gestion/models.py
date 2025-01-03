from django.utils import timezone
from django.db import models


# Create your models here.


    
class Service(models.Model):
    code = models.CharField(max_length=10, unique=True)  # Code du service
    description = models.CharField(max_length=100)  # Nom ou description du service

    def __str__(self):
        return self.description

class Employe(models.Model):
    code = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    daten = models.DateField(verbose_name="Date de Naissance")
    date_embauche = models.DateField(verbose_name="Date d'embauche")
    adresse = models.TextField()
    email = models.EmailField()
    telephone = models.CharField(max_length=15, null=True, blank=True)
    id_service = models.ForeignKey(Service, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"



class Conge(models.Model):
    TYPE_CONGE_CHOICES = [
        ('annuel', 'Congé Annuel'),
        ('maladie', 'Congé Maladie'),
        ('sans_solde', 'Congé Sans Solde'),
        ('maternite', 'Congé Maternité/Paternité'),
    ]

    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="conges")
    date_debut = models.DateField()
    date_fin = models.DateField()
    type_conge = models.CharField(max_length=50, choices=TYPE_CONGE_CHOICES)
    commentaire = models.TextField(null=True, blank=True)  # Détails supplémentaires

    def __str__(self):
        return f"Congé {self.type_conge} pour {self.employe.nom} du {self.date_debut} au {self.date_fin}"
    
    def duree_conge(self):
        """Calcule la durée en jours du congé."""
        return (self.date_fin - self.date_debut).days + 1

class SoldeConge(models.Model):
    employe = models.OneToOneField(Employe, on_delete=models.CASCADE, verbose_name="Employé", related_name="solde_conge")
    solde_annuel = models.IntegerField(default=30, verbose_name="Solde de Congés Annuels")
    solde_maladie = models.IntegerField(default=10, verbose_name="Solde de Congés Maladie")

    def __str__(self):
        return f"Solde des congés pour {self.employe.nom}"

    def deduire_solde(self, type_conge, jours):
        """Déduit les jours pris du solde de congés."""
        if type_conge == 'annuel':
            self.solde_annuel = max(self.solde_annuel - jours, 0)
        elif type_conge == 'maladie':
            self.solde_maladie = max(self.solde_maladie - jours, 0)
        self.save()

    def ajouter_solde(self, type_conge, jours):
        """Ajoute des jours au solde en cas d'annulation."""
        if type_conge == 'annuel':
            self.solde_annuel += jours
        elif type_conge == 'maladie':
            self.solde_maladie += jours
        self.save()

        
class Salaire(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="salaires")
    mois = models.DateField()  # Mois du salaire
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2)
    primes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    absences = models.IntegerField(default=0)  # Nombre de jours d'absence
    salaire_final = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Salaire de {self.employe.nom} pour {self.mois.strftime('%B %Y')}"


class Contrat(models.Model):
    TYPE_CONTRAT_CHOICES = [
        ('cdi', 'Contrat à Durée Indéterminée'),
        ('cdd', 'Contrat à Durée Déterminée'),
        ('stage', 'Stage'), 
    ]

    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="contrats")
    type_contrat = models.CharField(max_length=20, choices=TYPE_CONTRAT_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)  # Null si CDI
    salaire_mensuel = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"Contrat {self.type_contrat} pour {self.employe.nom}"

class Recrutement(models.Model):
    poste = models.CharField(max_length=100)  # Poste à pourvoir
    description = models.TextField()  # Description du poste
    date_publication = models.DateField()
    date_limite = models.DateField()

    def __str__(self):
        return f"Recrutement pour {self.poste}"


class Candidature(models.Model):
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    date_naissance = models.DateField(default='2000-01-01')  # Valeur par défaut
    genre = models.CharField(max_length=10, default='Non spécifié')  # Valeur par défaut
    email = models.EmailField()
    telephone = models.CharField(max_length=15)
    niveau = models.CharField(max_length=100)
    poste = models.CharField(max_length=100)
    cv = models.FileField(upload_to='uploads/cv/')
    motivation = models.FileField(upload_to='uploads/motivation/', default='uploads/motivation/default_motivation.pdf')  # Exemple de valeur par défaut
    date_soumission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.poste}"

class Evaluation(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="evaluations")
    date = models.DateField()
    note = models.DecimalField(max_digits=4, decimal_places=2)  # Note sur 10
    commentaire = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Évaluation de {self.employe.nom} ({self.date})"





