from django import forms
from .models import PatientProfile, PatientReport

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['name', 'last_name', 'age', 'gender', 'location', 'diseases', 'phone_number']


class PatientReportForm(forms.ModelForm):
    class Meta:
        model = PatientReport
        fields = ['name', 'last_name', 'age', 'gender', 'phone_number', 'dr_name', 'disease', 'precaution', 'medication']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'small-input'}),
            'last_name': forms.TextInput(attrs={'class': 'small-input'}),
            'age': forms.NumberInput(attrs={'class': 'small-input'}),
            'gender': forms.TextInput(attrs={'class': 'small-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'small-input'}),
            'dr_name': forms.TextInput(attrs={'class': 'small-input'}),
            'disease': forms.TextInput(attrs={'class': 'small-input'}),
           'precaution': forms.Textarea(attrs={'class': 'small-textarea', 'rows': 4, 'cols': 30}),  # Adjust rows and cols as needed
            'medication': forms.Textarea(attrs={'class': 'small-textarea', 'rows': 4, 'cols': 30}),  # Adjust rows and cols as needed
        
        }
    
