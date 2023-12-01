from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_username', 'patient_email')
    search_fields = ('patient_username', 'patient_email')
