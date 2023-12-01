from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('Prescription_success/', views.Prescription_success, name='Prescription_success'),
    path('login/forgot_password', views.forgot_password, name='forgot_password'),
    path('logoutuser/',views.my_logout_view, name='logout'),
    path('search_prescription/',views.search_prescription, name='search_prescription'),
    path('prescription/<int:prescription_id>/edit/', views.edit_prescription, name='edit_prescription'),
    path('prescription/<int:prescription_id>/delete/', views.delete_prescription, name='delete_prescription'),
    path('booking/<int:booking_id>/delete/', views.delete_booking, name='delete_booking'),
    path('prescription_pdf/<int:prescription_id>/download', views.prescription_pdf, name='prescription_pdf'),
    path('patient/login/', views.patient_login, name='patient_login'),
    path('patient/register/', views.patient_register, name='patient_register'),
    path('patient/logout/', views.patient_logout, name='patient_logout'),
    path('patient/index/', views.patient_index, name='patient_index'),  # Add the index URL
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
]
