# Gestion des Ressources Humaines: 

Ce projet de gestion des ressources humaines est une application web Django permettant de gérer les informations des employés, les recrutements, les candidatures, les contrats, les salaires, les congés.

## Fonctionnalités principales

### Gestion des Employés
- Ajouter, modifier et supprimer des employés.

### Gestion des Contrats
- Création de différents types de contrats : CDI, CDD, Stage.

### Recrutement et Candidatures
- Publier des offres d'emploi avec descriptions et dates limites.
- Suivre les candidatures avec leurs états : Reçu, En cours, Accepté, Rejeté.

### Congés
- Gérer les types de congés : annuel, maladie, maternité/paternité, sans solde.
- Suivre les soldes de congés restants pour chaque employé.

### Salaires
- Calcul automatique des salaires totaux avec :
  - Salaire de base.
  - Primes.
  - Heures supplémentaires.
  - Déductions pour congés sans solde.

### Évaluations
- Historique des évaluations des employés avec commentaires et notes.

### Tableau de bord RH
- Visualisation des données clés sous forme de tableaux et graphiques interactifs 

## Technologies utilisées
- **Backend** : Django (Python)
- **Frontend** : HTML, CSS, Bootstrap
- **Base de données** : SQLite (par défaut.)
- **Visualisation** : Matplotlib et Base64 pour génération de graphiques dynamiques.

## Installation

1. Clonez le projet :
   ```bash
   git clone https://github.com/samir15-ux/projet-SI.git
   cd gestion_rh
   ```

2. Créez et activez un environnement virtuel :
   ```bash
   Python –m venv env_rh
   env_rh\Scripts\activate
   cd gestion_rh
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Appliquez les migrations :
   ```bash
   python manage.py migrate
   ```

5. Lancez le serveur local :
   ```bash
   python manage.py runserver
   ```

6. Accédez à l'application :
   Ouvrez (http://127.0.0.1:8000/) dans votre navigateur.


## Améliorations futures
- Notifications automatiques pour les événements importants (fin de contrat, dates limites, etc.).
- Optimisation des graphiques pour une meilleure interactivité .
