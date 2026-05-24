from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, SeekerProfile, RecruiterProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a user profile when a new user is created.
    Depending on the role of the user (seeker or recruiter), it creates the appropriate profile.
     - If the user is a job seeker, it creates a SeekerProfile.
     - If the user is a recruiter, it creates a RecruiterProfile.
    This ensures that every user has a corresponding profile that can store additional information specific to their role.
    """
    if created:
        if instance.role == 'seeker':
            SeekerProfile.objects.create(user=instance)
        elif instance.role == 'recruiter':
            RecruiterProfile.objects.create(user=instance, company_name='')