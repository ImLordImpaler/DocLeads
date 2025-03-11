from django.db import models
# from django.contrib.auth.models import User
from accounts.models import User
from django.core.exceptions import ValidationError
from django.conf import settings

class Doctor(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    speciality = models.ForeignKey('Speciality' ,null=True, blank=True, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    years_of_experience = models.IntegerField(default=1)
    doc_image = models.CharField(max_length=200, default=settings.DEFAULT_IMAGE_URL)
    consulation_fee = models.IntegerField(default=100)
    doc_meta_data = models.JSONField(default=dict, blank=True)  # Store additional metadata as needed
    
    def __str__(self):
        return "Dr. {}".format(self.name)

class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='availabilities', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=9, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ])
    start_time = models.TimeField()  # Using time for more precise handling
    end_time = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['doctor', 'day_of_week', 'start_time', 'end_time'], name='unique_availability_slot')
        ]  # Prevents a doctor from having multiple availabilities for the same day
    
    def __str__(self):
        return f"{self.doctor.name} - {self.day_of_week}: {self.start_time} to {self.end_time}"
    
    def clean(self):
        # Check for overlapping time slots for the same doctor and day
        overlapping_slots = DoctorAvailability.objects.filter(
            doctor=self.doctor,
            day_of_week=self.day_of_week
        ).exclude(id=self.id)  # Exclude the current instance if it's being updated

        for slot in overlapping_slots:
            if (self.start_time < slot.end_time and self.end_time > slot.start_time):
                raise ValidationError("The time slot overlaps with an existing availability.")
            
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=10)

    paitent_meta_data = models.JSONField(default=dict, blank=True) 
    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    
    appointment_start_time = models.DateTimeField()  # Date and time of the appointment
    appointment_end_time = models.DateTimeField()
    def __str__(self):
        return f"Appointment with Dr. {self.doctor.name} at {self.appointment_start_time}"

class Speciality(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
