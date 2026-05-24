"""
Resume aggregate model plus nested entities: skills, languages, experience, education.
"""

from django.db import models
from django.conf import settings


class Resume(models.Model):
    """
    Model representing a candidate's resume, owned by a user with role 'candidate'.
    Includes nested related models for experience, education, skills, and languages.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    bio = models.TextField(blank=True)

    availability = models.CharField(max_length=100, blank=True)
    mobility = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class Experience(models.Model):
    """
    Model representing a candidate's work experience.
    """

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')

    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()


class Education(models.Model):
    """
    Model representing a candidate's educational background.
    """

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')

    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)


class Skill(models.Model):
    """
    Model representing a candidate's skill with a proficiency level.
    """
    
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')

    name = models.CharField(max_length=100)
    
    LEVEL_CHOICES = [
        (1, 'Beginner'),
        (2, 'Basic'),
        (3, 'Intermediate'),
        (4, 'Advanced'),
        (5, 'Expert'),
    ]

    level = models.IntegerField(choices=LEVEL_CHOICES)


class Language(models.Model):
    """
    Model representing a candidate's language proficiency.
    """

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='languages')

    name = models.CharField(max_length=100)
    
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('fluent', 'Fluent'),
        ('native', 'Native'),
    ]

    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)