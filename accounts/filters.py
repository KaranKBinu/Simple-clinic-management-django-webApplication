from django import forms
import django_filters
from home.models import Booking,Prescription


class DateInput(forms.DateInput):
    input_type = 'date'


class BookingFilter(django_filters.FilterSet):
    appointment_date = django_filters.DateFilter(widget=DateInput)

    class Meta:
        model = Booking
        fields = {
            'patient_name': ['icontains'],
            'patient_email': ['icontains'],
            'patient_phone': ['exact'],
            'patient_gender': ['exact'],
            'patient_age': ['exact', 'gte', 'lte'],
            'patient_type': ['exact'],
            'appointment_date': ['exact', 'gte', 'lte'],
        }








class PrescriptionFilter(django_filters.FilterSet):
    date_created = django_filters.DateFilter(widget=DateInput,field_name='date_created', lookup_expr='date')

    class Meta:
        model = Prescription
        fields = {
            'date_created': ['exact', 'gte', 'lte']
            }
