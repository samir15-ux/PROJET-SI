from django.forms import ValidationError
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User 



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
    departement = models.CharField(max_length=100)  
    poste = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def clean(self):
        if (timezone.now().date() - self.daten).days / 365 < 18:
            raise ValidationError("L'employé doit avoir au moins 18 ans.")


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
    poste = models.CharField(max_length=100)  
    description = models.TextField()  
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
    note = models.DecimalField(max_digits=4, decimal_places=2) 
    commentaire = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Évaluation de {self.employe.nom} ({self.date})"
    

class Conges(models.Model):
    TYPE_CONGE_CHOICES = [
        ('annuel', 'Congé Annuel'),
        ('maladie', 'Congé Maladie'),
        ('maternite', 'Congé Maternité/Paternité'),
        ('sans_solde', 'Congé Sans Solde'),
    ]
    
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    type_conge = models.CharField(max_length=20, choices=TYPE_CONGE_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.employe.nom} - {self.type_conge}"


class Salaire(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2)
    primes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    heures_supplementaires = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculer_salaire_total(self):
      solde_conge = SoldeConge.objects.filter(employe=self.employe).first()
      deduction_sans_solde = 0
      if solde_conge:
         deduction_sans_solde = solde_conge.solde_utilise_sans_solde * (self.salaire_base / 30)

      return self.salaire_base + self.primes + (self.heures_supplementaires * (self.salaire_base / 240)) - deduction_sans_solde  

    def __str__(self):
        return f"{self.employe.nom} - Salaire: {self.calculer_salaire_total()}"



class SoldeConge(models.Model):
    employe = models.OneToOneField(Employe, on_delete=models.CASCADE)
    solde_annuel = models.DecimalField(max_digits=5, decimal_places=2, default=30)  
    solde_maladie = models.DecimalField(max_digits=5, decimal_places=2, default=15)  
    solde_maternite = models.DecimalField(max_digits=5, decimal_places=2, default=20)  
    solde_sans_solde = models.DecimalField(max_digits=5, decimal_places=2, default=0) 
    solde_utilise_annuel = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    solde_utilise_maladie = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    solde_utilise_maternite = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    solde_utilise_sans_solde = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    @property
    def solde_restant_annuel(self):
        return self.solde_annuel - self.solde_utilise_annuel

    @property
    def solde_restant_maladie(self):
        return self.solde_maladie - self.solde_utilise_maladie

    @property
    def solde_restant_maternite(self):
        return self.solde_maternite - self.solde_utilise_maternite

    @property
    def solde_restant_sans_solde(self):
        return self.solde_utilise_sans_solde

    def __str__(self):
        return f"{self.employe.nom} - Soldes Restants: Annuel: {self.solde_restant_annuel}, Maladie: {self.solde_restant_maladie}, Maternité: {self.solde_restant_maternite}, Sans Solde: {self.solde_restant_sans_solde}"