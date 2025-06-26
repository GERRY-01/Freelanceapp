from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    
class Jobs(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.PositiveIntegerField()
    deadline = models.DateField()
    status = models.CharField(max_length=200, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def posted_at(self):
        now = timezone.now()
        diff = now - self.created_at
        if diff < timedelta(minutes=1):
            return 'just now'
        elif diff < timedelta(hours=1):
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif diff < timedelta(days=1):
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif now.date() - self.created_at.date() == 1:
            return "yesterday"
        else:
            return self.created_at.strftime("%b %d, %Y")
        
class Proposals(models.Model):
    freelancer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    proposal = models.TextField()
    budget = models.PositiveIntegerField()
    duration = models.PositiveIntegerField()
    portfolio_url = models.URLField(blank=True, null=True)
    attachment = models.FileField(upload_to='proposals/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
            