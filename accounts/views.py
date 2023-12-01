# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import PrescriptionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home.models import Doctors, Booking ,Prescription
from django.contrib.auth import logout
from django.db.models import Q
from .filters import BookingFilter



from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from django.utils import timezone
from reportlab.lib.units import inch
from reportlab.lib import colors

def prescription_pdf(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)

    # Set the font styles for the prescription
    c.setFont("Helvetica", 12)
    styles = getSampleStyleSheet()

    # Add the hospital logo and header
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(4.25 * inch, 10.75 * inch, "Co-operative Hospital")
    c.setFont("Helvetica", 12)
    c.drawCentredString(4.25 * inch, 10.5 * inch, "mullakkal, alappuzha, kerala INDIA")
    c.drawCentredString(4.25 * inch, 10.25 * inch, "Phone: 0477 235 335")
    c.drawCentredString(4.25 * inch, 10.0 * inch, "Mail: info@hospital.com")
    c.line(0.5 * inch, 9.75 * inch, 7.5 * inch, 9.75 * inch)

    # Retrieve prescription data
    patient_name = prescription.patient_name.patient_name
    doctor_name = prescription.doctor_name.doc_name
    medication = prescription.medication
    date_created = prescription.date_created.astimezone(timezone.get_current_timezone()).strftime('%d-%m-%Y %H:%M:%S') # Updated date format

    # Retrieve patient details from the Booking model
    booking = prescription.patient_name
    patient_age = booking.patient_age
    patient_gender = booking.get_patient_gender_display()
    patient_phone = booking.patient_phone

    # Define the prescription details
    details = [
        ("Prescribed By:", doctor_name),
        ("Patient Name:", patient_name),
        ("Patient Age:", str(patient_age)),
        ("Patient Gender:", patient_gender),
        ("Patient Phone:", patient_phone),
        ("Medication:", medication),
        ("Date:", date_created)
    ]

    # Set the styles for prescription details
    title_style = styles["Title"]
    title_style.fontSize = 14
    content_style = ParagraphStyle("Content", parent=styles["BodyText"], fontName="Helvetica-Bold")  # Set medication text to bold

    # Print the prescription details
    line_height = 0.5 * inch
    text_starting_point = 8.75 * inch

    c.saveState()  # Save the current state of the canvas

    # Add the watermark
    c.setFillColor(colors.lightgrey)
    c.setFont("Helvetica-Bold", 60)
    c.rotate(45)
    c.translate(-3.5 * inch, -3.5 * inch)  # Adjust the position of the watermark
    c.drawCentredString(9.25 * inch, 4.25 * inch, "Co-operative Hospital")

    c.restoreState()  # Restore the previous state of the canvas

    for title, content in details:
        title_paragraph = Paragraph(f"<b>{title}</b>", title_style)
        content_paragraph = Paragraph(content, content_style)

        if title == "Medication:":
            title_paragraph.wrapOn(c, 5 * inch, line_height)
            content_paragraph.wrapOn(c, 5 * inch, line_height)
            title_paragraph.drawOn(c, 2.25 * inch, text_starting_point)
            content_paragraph.drawOn(c, 2.25 * inch, text_starting_point - line_height)
            text_starting_point -= 1.5 * line_height
        elif title == "Date:":
            title_paragraph.wrapOn(c, 2 * inch, line_height)
            content_paragraph.wrapOn(c, 2 * inch, line_height)
            title_paragraph.drawOn(c, 5.5 * inch, 0.75 * inch)
            content_paragraph.drawOn(c, 7.0 * inch, 0.85 * inch)
        else:
            title_paragraph.wrapOn(c, 2 * inch, line_height)
            content_paragraph.wrapOn(c, 2 * inch, line_height)
            title_paragraph.drawOn(c, 0.5 * inch, text_starting_point)
            content_paragraph.drawOn(c, 2.5 * inch, text_starting_point)
            text_starting_point -= line_height

    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='prescription.pdf')

@login_required
def doctor_dashboard(request):
    filter = BookingFilter(request.GET, queryset=Booking.objects.all())
    user = request.user
    doctors = Doctors.objects.all()
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Prescription_success')
    else:

        form = PrescriptionForm()

    return render(request, 'accounts/doctor_dashboard.html', {'doctors': doctors, 'form': form, 'filter': filter})


from .filters import PrescriptionFilter

@login_required
def Prescription_success(request):
    doctors = Doctors.objects.all()
    prescription = Prescription.objects.all()
    prescription_filter = PrescriptionFilter(request.GET, queryset=prescription)
    return render(request, 'accounts/Prescription_success.html', {'doctors': doctors, 'prescription': prescription_filter})


@login_required
def edit_prescription(request, prescription_id):
    prescription = Prescription.objects.get(id=prescription_id)
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect('Prescription_success')
    else:
        form = PrescriptionForm(instance=prescription)
    
    return render(request, 'accounts/edit_prescription.html', {'form': form})
    

@login_required  
def my_logout_view(request):
    logout(request)
    return redirect('login')


def forgot_password(request):
  return render(request,'accounts/forgot_password.html')
  
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('doctor_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


from django.db.models import Q
@login_required
def search_prescription(request):
    if request.method == "POST":
        searched = request.POST['searched']
        prescriptions = Prescription.objects.filter(
            Q(medication__contains=searched) |
            Q(patient_name__patient_name__contains=searched) 
        )
        return render(request,'accounts/search_prescription.html',{'searched':searched, 'prescriptions':prescriptions})
    else:
        return render(request,'accounts/search_prescription.html')
        
from django.shortcuts import get_object_or_404, redirect


@login_required
def delete_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    
    if request.method == 'POST':
        prescription.delete()
        return redirect('Prescription_success')
    
    return render(request, 'accounts/delete_prescription.html', {'prescription': prescription})
    

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        # Handle the form submission for deleting the booking
        booking.delete()
        return redirect('patient_index')
    
    return render(request, 'accounts/cancel_booking.html', {'booking': booking})
    
    
 
@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        # Handle the form submission for deleting the booking
        booking.delete()
        return redirect('doctor_dashboard')
    
    return render(request, 'accounts/delete_booking.html', {'booking': booking})
    
    
 


from .models import Patient



def patient_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']

        if password != confirm_password:
            error_message = 'Passwords do not match.'
            return render(request, 'accounts/patient_register.html', {'error_message': error_message})

        try:
            patient = Patient.objects.create(patient_username=username, patient_password=password, patient_email=email)
            # Optionally, log the patient in automatically after registration
            return redirect('patient_index')  # Replace 'home' with your desired URL after registration success
        except:
            error_message = 'username or email already exists'
            return render(request, 'accounts/patient_register.html', {'error_message': error_message})
    
    return render(request, 'accounts/patient_register.html')




from django.shortcuts import render, redirect
from home.models import Prescription, Booking
from accounts.models import Patient

def patient_index(request):
    if not request.session.get('patient_id'):
        return redirect('patient_login')

    patient_id = request.session['patient_id']
    patient = Patient.objects.get(id=patient_id)
    prescriptions = Prescription.objects.filter(patient_name__patient_name=patient.patient_username)
    bookings = Booking.objects.filter(patient_name=patient.patient_username)
    return render(request, 'accounts/patient_index.html', {'patient': patient, 'prescriptions': prescriptions, 'bookings':bookings})

def patient_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            patient = Patient.objects.get(patient_username=username, patient_password=password)
            # Store patient ID in session
            request.session['patient_id'] = patient.id
            return redirect('patient_index')
        except Patient.DoesNotExist:
            error_message = 'Invalid username or password.'
            return render(request, 'accounts/patient_login.html', {'error_message': error_message})
    return render(request, 'accounts/patient_login.html')



def patient_logout(request):
    if request.session.get('patient_id'):
        # Perform logout operations
        del request.session['patient_id']
    return redirect('index')
