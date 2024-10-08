from django.db import models



class DoctorProfile(models.Model):

    doctor_name = models.CharField(max_length=100, null=True, blank=True)
    doctor_image = models.ImageField(upload_to='doctor_images/')
    doctor_timings = models.DateTimeField()
    doctor_bio = models.CharField(max_length=255)  # Specify the max_length for CharField
    doctor_room_id = models.CharField(max_length=20,null=True, blank=True) 
    doctor_phone_number = models.CharField(max_length=20,null=True, blank=True)  # Assuming maximum length for phone number
    doctor_language=models.CharField(max_length=20)
    doctor_speciality=models.CharField(max_length=30)
    def __str__(self):
        return self.doctor_name


# class GetHealthTruck(models.Model):
#     user_location = models.CharField()

class PatientEducation(models.Model):
    topic = models.CharField(max_length=20)
    url = models.URLField(max_length=100)
    
    def __str__(self):
        return f'{self.topic} - {self.url}'


from django.db import models
from social_django.models import UserSocialAuth

class PatientProfile(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    location = models.CharField(max_length=100)
    diseases = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name} {self.last_name}'

from django.db import models
from social_django.models import UserSocialAuth

class PatientReport(models.Model):
   
    dr_name = models.CharField(max_length=200)
    disease = models.CharField(max_length=200)
    precaution = models.TextField()
    medication = models.TextField()
    
    # New fields
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)  # Assuming limited options like 'Male', 'Female', 'Other'
    phone_number = models.CharField(max_length=20)  # Adjust max_length as per your requirements

    def __str__(self):
        return f'{self.name} {self.last_name} - {self.disease}'


