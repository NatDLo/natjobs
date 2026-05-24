"""
Job application model linking seeker, job, and submitted resume.
Includes application status and optional notes for tracking the application process.
"""

from django.db import models
from django.conf import settings
from jobs.models import Job
from resumes.models import Resume

class Application(models.Model):
    """
    Model representing a job application submitted by a seeker.
    Links the seeker, the job, and the resume used for the application.
    """

    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('reviewing', 'Reviewing'),
        ('interview', 'Interview'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    seeker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.seeker.username} → {self.job.title}"