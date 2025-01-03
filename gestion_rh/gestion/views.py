import base64
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
import matplotlib.pyplot as plt
from django.contrib.auth.decorators import login_required


from .forms import CongeForm, ContratForm, EmployeForm, EvaluationForm,  RecrutementForm, SalaireForm, ServiceForm, SoldeCongeForm
from .models import Candidature, Employe, Evaluation, Recrutement, Salaire, Service, Conge, Contrat, SoldeConge

# Create your views here.



def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige vers la page de connexion après inscription
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})



def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/gestion/dashboard/')  # Redirection après connexion réussie
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/gestion/login/')

def index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    return render(request,'dashboard.html')

def postuler(request):
    if request.method == "POST":
        prenom = request.POST['prenom']
        nom = request.POST['nom']
        date_naissance = request.POST['date_naissance']
        genre = request.POST['genre']
        email = request.POST['email']
        telephone = request.POST['telephone']
        niveau = request.POST['niveau']
        poste = request.POST['poste']
        cv = request.FILES['cv']
        motivation = request.FILES['motivation']

        # Sauvegarder les données dans la base
        candidature = Candidature(
            prenom=prenom,
            nom=nom,
            date_naissance=date_naissance,
            genre=genre,
            email=email,
            telephone=telephone,
            niveau=niveau,
            poste=poste,
            cv=cv,
            motivation=motivation
        )
        candidature.save()

        return HttpResponse("Candidature soumise avec succès !")
    return render(request, 'postuler.html')

def gestion_tables(request):
    employes = Employe.objects.all()
    services = Service.objects.all()
    conges = Conge.objects.all()
    contrats = Contrat.objects.all()
    
    return render(request, 'gestion_tables.html', {
        'employes': employes,
        'services': services,
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





def gestion_services(request):
    search_query = request.GET.get('search', '')
    services = Service.objects.filter(description__icontains=search_query) if search_query else Service.objects.all()
    return render(request, 'gestion_services/service_list.html', {'services': services})

def ajouter_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_services')
    else:
        form = ServiceForm()
    return render(request, 'gestion_services/service_form.html', {'form': form, 'action': 'Ajouter'})

def modifier_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('gestion_services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'gestion_services/service_form.html', {'form': form, 'action': 'Modifier'})

def supprimer_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('gestion_services')
    return render(request, 'gestion_services/service_confirm_delete.html', {'service': service})






def gestion_conges(request):
    search_query = request.GET.get('search', '')
    conges = Conge.objects.filter(employe__nom__icontains=search_query) if search_query else Conge.objects.all()
    return render(request, 'gestion_conges/conge_list.html', {'conges': conges})

def ajouter_conge(request):
    if request.method == 'POST':
        form = CongeForm(request.POST)
        if form.is_valid():
            form.save()
            solde = SoldeConge.objects.get(employe=Conge.employe)
            solde.deduire_solde(Conge.type_conge, Conge.duree_conge())
            return redirect('gestion_conges')
    else:
        form = CongeForm()
    return render(request, 'gestion_conges/conge_form.html', {'form': form, 'action': 'Ajouter'})

def modifier_conge(request, pk):
    conge = get_object_or_404(Conge, pk=pk)
    if request.method == 'POST':
        form = CongeForm(request.POST, instance=conge)
        if form.is_valid():
            form.save()
            return redirect('gestion_conges')
    else:
        form = CongeForm(instance=conge)
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



