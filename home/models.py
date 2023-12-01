from django.db import models

# Create your models here.

class Departments(models.Model):
    dep_name = models.CharField(max_length=50)
    dep_description = models.TextField()
    def __str__(self):
        return self.dep_name

class Doctors(models.Model):
    doc_name = models.CharField(max_length=255)
    doc_spec = models.CharField(max_length=255)
    dep_name = models.ForeignKey(Departments, on_delete=models.CASCADE)
    doc_image = models.ImageField(upload_to='doctors')
    def __str__(self):
        return f"Dr. {self.doc_name} - {self.doc_spec}"

class Booking(models.Model):
    
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    patient_phone =models.CharField(max_length=15)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('TM', 'Trans Men'),
        ('TW', 'Trans Women'),
        ('O', 'Other'),
    ]
    patient_gender = models.CharField(max_length=2, choices=GENDER_CHOICES,default='')
    AGE_CHOICES = [(i, str(i)) for i in range(0, 151)]
    patient_age = models.IntegerField(choices=AGE_CHOICES, default=0)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    PATIENT_CHOICES = [
    ('Normal Patient- I can visit the hospital', 'Normal Patient- I can visit the hospital'),
    ('Bedridden Patient', 'Bedridden Patient'),
    ('Pregnant Lady', 'Pregnant Lady'),
    ('Other - I can not visit the Hospital', 'Other - I can not visit the Hospital'),
    ('Need Online consultancy', 'Need Online consultancy'),
    ]
    patient_type = models.CharField(max_length=50, choices=PATIENT_CHOICES, default='select patient type')

    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    booked_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.patient_name

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name
       
       
class Prescription(models.Model):
    patient_name = models.ForeignKey(Booking, on_delete=models.CASCADE)
    doctor_name = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    medication = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.medication} - {self.date_created}"