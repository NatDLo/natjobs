from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    """
    Extend the default Django User model to include a role field that distinguishes between recruiters and job seekers.
    This allows us to easily manage different types of users in our application.
    """
    ROLE_CHOICES = (
        ('recruiter', 'Recruiter'),
        ('seeker', 'Job Seeker'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


class SeekerProfile(models.Model):
    """
    Profile model for job seekers, extending the custom User model.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Seeker: {self.user.username}"


class RecruiterProfile(models.Model):
    """
    Profile model for recruiters, extending the custom User model.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Recruiter: {self.user.username}"