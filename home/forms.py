from django import forms
from .models import Booking,Contact,Prescription
class BookingForm(forms.ModelForm):
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'DD-MM-YYYY'
        })
    )
    appointment_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
            'placeholder': 'HH:MM'
        })
    )

    class Meta:
  
        model =Booking
        exclude = ['booked_on']
        fields = ['patient_name', 'patient_email', 'patient_phone','patient_gender','patient_age','patient_type', 'doctor', 'appointment_date', 'appointment_time']
        

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
       
       
       
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient_name', 'doctor_name', 'medication']