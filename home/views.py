from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Departments,Doctors
from .models import Contact,Booking
from .forms import BookingForm
from .forms import ContactForm
from .forms import PrescriptionForm
from .models import Prescription


def index(request):
    departments = Departments.objects.all()
    context = {'departments': departments}
    return render(request, 'index.html', context)
   

def about(request):
    context = {
        'page_title': 'About Us',
    }
    return render(request, 'about.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = 'Your message has been sent!'
            form = ContactForm()  # reset form after successful submission
        else:
            success_message = None
    else:
        form = ContactForm()
        success_message = None
    return render(request, 'contact.html', {'form': form, 'success_message': success_message})


def Department(request):
    dect_dept={
      'dept': Departments.objects.all()
    }
    return render(request, 'department.html',dect_dept)



def Doctor(request):
    dect_docs={
      'doctors': Doctors.objects.all()
    }
    return render(request, 'doctors.html', dect_docs)

from accounts.models import Patient

def booking(request):
    if not request.session.get('patient_id'):
        return redirect('patient_login')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_success')
        else:
            messages.error(request, 'Booking failed.')
    else:
        form = BookingForm()

    return render(request, 'booking.html', {'form': form})

    



def booking_success(request):
    latest_booking = Booking.objects.latest('id')
    context = {'booking': latest_booking}
    return render(request, 'booking_success.html', context)
