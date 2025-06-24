from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CustomUser(models.Model):
    user = models.oneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200)
    ROLE = (
        ('freelancer', 'freelancer'),
        ('client', 'client'),
    )
    
    account_type = models.CharField(max_length=20, choices=ROLE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    
    #client specific
    company_name = models.CharField(max_length=200, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
     
    SIZE = (
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('200+', '200+ employees'),
    )
        
    company_size = models.CharField(max_length=20, choices=SIZE, blank=True, null=True) 
    
    #freelancer specific
    skills = models.CharField(max_length=200, blank=True, null=True)
    experience = models.PositiveIntegerField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)