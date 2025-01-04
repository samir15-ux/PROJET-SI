from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .forms import CandidatureForm, CongeForm, ContratForm, EmployeForm, EvaluationForm,  RecrutementForm, SalaireForm, SoldeCongeForm, congeForm
from .models import Employe, Evaluation, Recrutement, Salaire, Conge, Contrat, SoldeConge

# Create your views here.


def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        code_employe = request.POST.get('code_employe')  # Récupérer le code employé depuis le formulaire

        try:
            # Vérifiez que le code employé existe dans la base de données
            employe = Employe.objects.get(code=code_employe)
        except Employe.DoesNotExist:
            # Si le code employé est invalide, affichez un message d'erreur
            messages.error(request, "Le code employé est invalide. Veuillez réessayer.")
            return render(request, 'register.html', {'form': form})
        
        if form.is_valid():
            # Si tout est valide, sauvegardez le nouvel utilisateur
            user = form.save()
            messages.success(request, "Inscription réussie !")
            return redirect('login')  # Redirige vers la page de connexion
    
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})



def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authentifier l'utilisateur
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Redirection basée sur le rôle
            if user.is_staff:  # Agent RH
                return redirect('/gestion/dashboard/')  # Redirige vers l'administration Django
            else:  # Employé
                return redirect('/gestion/employe/dashboard/')  # Redirige vers le tableau de bord employé
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    
    # Afficher la page de connexion
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/gestion/login/')

def index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    return render(request,'dashboard.html')



def gestion_tables(request):
    employes = Employe.objects.all()
    conges = Conge.objects.all()
    contrats = Contrat.objects.all()
    
    return render(request, 'gestion_tables.html', {
        'employes': employes,
        'conges': conges,
        'contrats': contrats
    })

def gestion_employes(request):
    search_query = request.GET.get('search', '')
    if search_query:
        employes = Employe.objects.filter(nom__icontains=search_query)  # Recherche par nom
    else:
        employes = Employe.objects.all()

    return render(request, 'gestion_employes/employe_list.html', {'employes': employes, 'search_query': search_query})


def ajouter_employe(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_employes')
    else:
        form = EmployeForm()
    return render(request, 'gestion_employes/employe_form.html', {'form': form, 'action': 'Ajouter'})



def modifier_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()
            return redirect('gestion_employes')
    else:
        form = EmployeForm(instance=employe)
    return render(request, 'gestion_employes/employe_form.html', {'form': form, 'action': 'Modifier'})


def supprimer_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        employe.delete()
        return redirect('gestion_employes')
    return render(request, 'gestion_employes/employe_confirm_delete.html', {'employe': employe})



def gestion_conges(request):
    search_query = request.GET.get('search', '')
    conges = Conge.objects.filter(employe__nom__icontains=search_query) if search_query else Conge.objects.all()
    return render(request, 'gestion_conges/conge_list.html', {'conges': conges})

def ajouter_conge(request):
    if request.method == 'POST':
        form = congeForm(request.POST)
        if form.is_valid():
            form.save()
            solde = SoldeConge.objects.get(employe=Conge.employe)
            solde.deduire_solde(Conge.type_conge, Conge.duree_conge())
            return redirect('gestion_conges')
    else:
        form = congeForm()
    return render(request, 'gestion_conges/conge_form.html', {'form': form, 'action': 'Ajouter'})

def modifier_conge(request, pk):
    conge = get_object_or_404(Conge, pk=pk)
    if request.method == 'POST':
        form = congeForm(request.POST, instance=conge)
        if form.is_valid():
            form.save()
            return redirect('gestion_conges')
    else:
        form = congeForm(instance=conge)
    return render(request, 'gestion_conges/conge_form.html', {'form': form, 'action': 'Modifier'})


def supprimer_conge(request, pk):
    conge = get_object_or_404(Conge, pk=pk)
    if request.method == 'POST':
        solde = SoldeConge.objects.get(employe=conge.employe)
        solde.ajouter_solde(conge.type_conge, conge.duree_conge())
        conge.delete()
        return redirect('gestion_conges')
    return render(request, 'gestion_conges/conge_confirm_delete.html', {'conge': conge})




def gestion_salaires(request):
    search_query = request.GET.get('search', '')
    salaires = Salaire.objects.filter(employe__nom__icontains=search_query) if search_query else Salaire.objects.all()
    return render(request, 'gestion_salaires/salaire_list.html', {'salaires': salaires})


def ajouter_salaire(request):
    if request.method == 'POST':
        form = SalaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_salaires')
    else:
        form = SalaireForm()
    return render(request, 'gestion_salaires/salaire_form.html', {'form': form, 'action': 'Ajouter'})

def modifier_salaire(request, pk):
    salaire = get_object_or_404(Salaire, pk=pk)
    if request.method == 'POST':
        form = SalaireForm(request.POST, instance=salaire)
        if form.is_valid():
            form.save()
            return redirect('gestion_salaires')
    else:
        form = SalaireForm(instance=salaire)
    return render(request, 'gestion_salaires/salaire_form.html', {'form': form, 'action': 'Modifier'})

def supprimer_salaire(request, pk):
    salaire = get_object_or_404(Salaire, pk=pk)
    if request.method == 'POST':
        salaire.delete()
        return redirect('gestion_salaires')
    return render(request, 'gestion_salaires/salaire_confirm_delete.html', {'salaire': salaire})


def gestion_contrats(request):
    search_query = request.GET.get('search', '')
    contrats = Contrat.objects.filter(employe__nom__icontains=search_query) if search_query else Contrat.objects.all()
    return render(request, 'gestion_contrats/contrat_list.html', {'contrats': contrats})

def ajouter_contrat(request):
    if request.method == 'POST':
        form = ContratForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_contrats')
    else:
        form = ContratForm()
    return render(request, 'gestion_contrats/contrat_form.html', {'form': form, 'action': 'Ajouter'})

def modifier_contrat(request, pk):
    contrat = get_object_or_404(Contrat, pk=pk)
    if request.method == 'POST':
        form = ContratForm(request.POST, instance=contrat)
        if form.is_valid():
            form.save()
            return redirect('gestion_contrats')
    else:
        form = ContratForm(instance=contrat)
    return render(request, 'gestion_contrats/contrat_form.html', {'form': form, 'action': 'Modifier'})

def supprimer_contrat(request, pk):
    contrat = get_object_or_404(Contrat, pk=pk)
    if request.method == 'POST':
        contrat.delete()
        return redirect('gestion_contrats')
    return render(request, 'gestion_contrats/contrat_confirm_delete.html', {'contrat': contrat})





def gestion_recrutements(request):
    search_query = request.GET.get('search', '')
    recrutements = Recrutement.objects.filter(poste__icontains=search_query) if search_query else Recrutement.objects.all()
    return render(request, 'gestion_recrutements/recrutement_list.html', {'recrutements': recrutements})


def ajouter_recrutement(request):
    if request.method == 'POST':
        form = RecrutementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_recrutements')
    else:
        form = RecrutementForm()
    return render(request, 'gestion_recrutements/recrutement_form.html', {'form': form, 'action': 'Ajouter'})

def modifier_recrutement(request, pk):
    recrutement = get_object_or_404(Recrutement, pk=pk)
    if request.method == 'POST':
        form = RecrutementForm(request.POST, instance=recrutement)
        if form.is_valid():
            form.save()
            return redirect('gestion_recrutements')
    else:
        form = RecrutementForm(instance=recrutement)
    return render(request, 'gestion_recrutements/recrutement_form.html', {'form': form, 'action': 'Modifier'})

def supprimer_recrutement(request, pk):
    recrutement = get_object_or_404(Recrutement, pk=pk)
    if request.method == 'POST':
        recrutement.delete()
        return redirect('gestion_recrutements')
    return render(request, 'gestion_recrutements/recrutement_confirm_delete.html', {'recrutement': recrutement})



def Gestion_personnel(request):
    employes = Employe.objects.all()  # Récupère tous les employés
    return render(request, 'Gestion_personnel/personnel_list.html', {'employes': employes})


def fiche_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    evaluations = Evaluation.objects.filter(employe=employe)
    return render(request, 'Gestion_personnel/fiche_employe.html', {'employe': employe, 'evaluations': evaluations})



def ajouter_evaluation(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == "POST":
        form = EvaluationForm(request.POST) 
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.employe = employe
            evaluation.save()
            return redirect('fiche_employe', pk=employe.pk)
    else:
        form = EvaluationForm()
    return render(request, 'Gestion_personnel/ajouter_evaluation.html', {'form': form, 'employe': employe})

def solde_conge_list(request):
    soldes = SoldeConge.objects.all()
    return render(request, "gestion_conges/solde_conge_list.html", {"soldes": soldes})

def solde_conge_update(request, employe_id):
    solde = get_object_or_404(SoldeConge, employe_id=employe_id)
    if request.method == "POST":
        form = SoldeCongeForm(request.POST, instance=solde)
        if form.is_valid():
            form.save()
            return redirect("solde_conge_list")
    else:
        form = SoldeCongeForm(instance=solde)
    return render(request, "gestion_conges/solde_conge_form.html", {"form": form, "solde": solde})

def postuler(request):
    if request.method == 'POST':
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CandidatureForm()
    return render(request, 'postuler.html', {'form': form})

from django.contrib import messages

@login_required
def employe_dashboard(request):
    try:
        # Récupérer l'employé associé à l'utilisateur connecté
        employe = Employe.objects.get(user=request.user)  # L'utilisateur connecté doit avoir une relation avec l'employé
    except Employe.DoesNotExist:
        employe = None  # Si aucun employé n'est trouvé, vous pouvez gérer cette situation comme vous voulez
    
    return render(request, 'employe_dashboard.html', {'employe': employe})

def demande_conge(request):
    if not request.user.is_authenticated:
        messages.error(request, "Vous devez être connecté pour soumettre une demande de congé.")
        return redirect("login")  # Ou une redirection appropriée

    # Vérifier si l'utilisateur a bien un employé associé
    if not hasattr(request.user, 'employe') or request.user.employe is None:
        messages.error(request, "Aucun employé associé à votre compte.")
        return redirect("home")  # Ou une redirection appropriée

    if request.method == "POST":
        form = CongeForm(request.POST)
        if form.is_valid():
            conge = form.save(commit=False)
            conge.employe = request.user.employe  # Associer l'employé connecté
            try:
                conge.clean()  # Valider les règles métier (dates, solde)
                conge.save()  # Sauvegarder si tout est valide
                messages.success(request, "Votre demande de congé a été soumise avec succès.")
                return redirect("consulter_conges")  # Rediriger vers la liste des congés
            except ValidationError as e:
                form.add_error(None, e)  # Ajouter l'erreur au formulaire
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = CongeForm()

    return render(request, "gestion_conges/demande_conge.html", {"form": form})

def consulter_conges(request):
    conges = Conge.objects.filter(employe=request.user.employe).order_by('-date_debut')
    return render(request, "gestion_conges/consulter_conges.html", {"conges": conges})

