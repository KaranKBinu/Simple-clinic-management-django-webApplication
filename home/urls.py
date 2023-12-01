from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('booking/', views.booking, name='booking'), 
    path('doctors/', views.Doctor, name='Doctor'),
    path('departments/', views.Department, name='Department'),
    path('booking_success/', views.booking_success, name='booking_success'),
    
    
    
]