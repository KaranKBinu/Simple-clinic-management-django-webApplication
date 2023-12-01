from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from home.models import Doctors,Booking, Prescription 


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient_name', 'doctor_name', 'medication']
