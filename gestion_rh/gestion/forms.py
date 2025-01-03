from django import forms
from django.contrib.auth.models import User
from .models import  Employe, Evaluation,  Service, Conge, Contrat, Salaire, Recrutement, SoldeConge

class UserCreationForm (forms.ModelForm):
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmation du mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return password2



class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = '__all__'

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe 
        fields = '__all__'

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['code', 'description']

class CongeForm(forms.ModelForm):
    class Meta:
        model = Conge
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get("date_debut")
        date_fin = cleaned_data.get("date_fin")
        if date_debut and date_fin and date_debut > date_fin:
            raise forms.ValidationError("La date de fin doit être après la date de début.")
        return cleaned_data      
    
class SoldeCongeForm(forms.ModelForm):
    class Meta:
        model = SoldeConge
        fields = ["solde_annuel", "solde_maladie"]

class ContratForm(forms.ModelForm):
    class Meta:
        model = Contrat
        fields = '__all__'

class SalaireForm(forms.ModelForm):
    class Meta:
        model = Salaire
        fields = '__all__'

class RecrutementForm(forms.ModelForm):
    class Meta:
        model = Recrutement
        fields = '__all__'




