
from django.db import models

class Patient(models.Model):
    patient_username = models.CharField(max_length=100, unique=True)
    patient_password = models.CharField(max_length=100)
    patient_email = models.EmailField(max_length=100,unique=True)

    def __str__(self):
        return self.patient_username
