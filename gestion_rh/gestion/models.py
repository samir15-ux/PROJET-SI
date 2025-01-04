from django.forms import ValidationError
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employe", null=True, blank=True)  
    code = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    daten = models.DateField(verbose_name="Date de Naissance")
    date_embauche = models.DateField(verbose_name="Date d'embauche")
    adresse = models.TextField()
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    departement = models.CharField(max_length=100)  # Département
    poste = models.CharField(max_length=100)  # Poste

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def clean(self):
        if (timezone.now().date() - self.daten).days / 365 < 18:
            raise ValidationError("L'employé doit avoir au moins 18 ans.")




class Conge(models.Model):
    TYPE_CONGE_CHOICES = [
        ('annuel', 'Congé Annuel'),
        ('maladie', 'Congé Maladie'),
        ('sans_solde', 'Congé Sans Solde'),
        ('maternite', 'Congé Maternité/Paternité'),
    ]

    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    type_conge = models.CharField(max_length=50, choices=TYPE_CONGE_CHOICES)
    commentaire = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Congé {self.type_conge} pour {self.employe.nom} du {self.date_debut} au {self.date_fin}"

    def duree_conge(self):
        return (self.date_fin - self.date_debut).days + 1

    def clean(self):
        if self.date_fin < self.date_debut:
            raise ValidationError("La date de fin doit être après la date de début.")
            
        if self.type_conge in ['annuel', 'maladie']:
            if not self.employe:
               raise ValidationError("This conge must be associated with an employe.")
            solde = getattr(self.employe.solde_conge, f"solde_{self.type_conge}", 0)
            if self.duree_conge() > solde:
                raise ValidationError(f"Solde insuffisant pour un congé {self.type_conge}.")


class SoldeConge(models.Model):
    employe = models.OneToOneField(Employe, on_delete=models.CASCADE, verbose_name="Employé", related_name="solde_conge")
    solde_annuel = models.IntegerField(default=30, verbose_name="Solde de Congés Annuels")
    solde_maladie = models.IntegerField(default=10, verbose_name="Solde de Congés Maladie")

    def __str__(self):
        return f"Solde des congés pour {self.employe.nom}"

    def mettre_a_jour_solde(self, type_conge, jours, operation='deduire'):
        solde_attr = f"solde_{type_conge}"
        if not hasattr(self, solde_attr):
            raise ValueError("Type de congé invalide.")
        solde_actuel = getattr(self, solde_attr, 0)
        if operation == 'deduire':
            setattr(self, solde_attr, max(solde_actuel - jours, 0))
        elif operation == 'ajouter':
            setattr(self, solde_attr, solde_actuel + jours)
        self.save()


        
class Salaire(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="salaires")
    mois = models.DateField()  # Mois du salaire
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2)
    primes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    absences = models.IntegerField(default=0)
    salaire_final = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def __str__(self):
        return f"Salaire de {self.employe.nom} pour {self.mois.strftime('%B %Y')}"

    def save(self, *args, **kwargs):
        self.salaire_final = self.salaire_base + self.primes - (self.absences * (self.salaire_base / 30))
        super().save(*args, **kwargs)



class Contrat(models.Model):
    TYPE_CONTRAT_CHOICES = [
        ('cdi', 'Contrat à Durée Indéterminée'),
        ('cdd', 'Contrat à Durée Déterminée'),
        ('stage', 'Stage'),
    ]

    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="contrats")
    type_contrat = models.CharField(max_length=20, choices=TYPE_CONTRAT_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    salaire_mensuel = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Contrat {self.type_contrat} pour {self.employe.nom}"

    def clean(self):
        if self.type_contrat == 'cdi' and self.date_fin is not None:
            raise ValidationError("Un contrat CDI ne peut pas avoir de date de fin.")


class Recrutement(models.Model):
    poste = models.CharField(max_length=100)  # Poste à pourvoir
    description = models.TextField()  # Description du poste
    date_publication = models.DateField()
    date_limite = models.DateField()

    def __str__(self):
        return f"Recrutement pour {self.poste}"


class Candidature(models.Model):
    recrutement = models.ForeignKey(Recrutement, on_delete=models.CASCADE, related_name="candidatures")
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    genre = models.CharField(max_length=10, choices=[('Homme', 'Homme'), ('Femme', 'Femme')], default='Homme')
    date_naissance = models.DateField(null=True, blank=True)
    email = models.EmailField()
    telephone = models.CharField(max_length=15, null=True, blank=True)
    niveau_etude = models.CharField(max_length=50, null=True, blank=True)
    lettre_motivation = models.FileField(upload_to='lettres/', null=True, blank=True)
    cv = models.FileField(upload_to='cvs/')
    etat = models.CharField(max_length=20, choices=[
        ('reçu', 'Reçu'),
        ('en_cours', 'En cours de traitement'),
        ('accepté', 'Accepté'),
        ('rejeté', 'Rejeté'),
    ], default='reçu')

    def __str__(self):
     return f"{self.nom} {self.prenom} - {self.etat} ({self.recrutement.poste})"




    


class Evaluation(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="evaluations")
    date = models.DateField()
    note = models.DecimalField(max_digits=4, decimal_places=2)  # Note sur 10
    commentaire = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Évaluation de {self.employe.nom} ({self.date})"




