from django.contrib import admin
from .models import Departments,Doctors,Booking,Contact,Prescription
# Register your models here.
admin.site.register(Departments)
admin.site.register(Doctors)

class BookingAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'patient_email', 'patient_phone','patient_age','patient_gender', 'doctor', 'appointment_date', 'appointment_time', 'booked_on']
    search_fields = ['patient_name', 'patient_email']

admin.site.register(Booking, BookingAdmin)

class ContactAdmin(admin.ModelAdmin):
  list_display = ['name','email','subject','message']
admin.site.register(Contact,ContactAdmin)

class PrescriptionAdmin(admin.ModelAdmin):
  list_display = ['patient_name','doctor_name','medication','date_created']
admin.site.register(Prescription,PrescriptionAdmin)
