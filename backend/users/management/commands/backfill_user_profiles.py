"""
Management command to backfill missing seeker/recruiter profiles for existing users.
This command iterates through all users in the database and checks if they have the appropriate profile based on their role.
If a user with the "seeker" role is missing a SeekerProfile, it creates one. Similarly, if a user with the "recruiter" role is
missing a RecruiterProfile, it creates one with an empty company name. This ensures that all users have the necessary profiles
for their respective roles, allowing the application to function correctly without errors related to missing profiles.
"""

from django.core.management.base import BaseCommand

from users.models import RecruiterProfile, SeekerProfile, User


class Command(BaseCommand):
    """
    Django management command to backfill missing seeker/recruiter profiles for existing users.
    """

    help = "Create missing seeker/recruiter profiles for existing users."

    def handle(self, *args, **options):
        """
        Iterate through all users and create missing profiles based on their role.
        """

        created_seeker = 0
        created_recruiter = 0

        for user in User.objects.all():
            if user.role == "seeker":
                _, created = SeekerProfile.objects.get_or_create(user=user)
                if created:
                    created_seeker += 1

            elif user.role == "recruiter":
                _, created = RecruiterProfile.objects.get_or_create(
                    user=user,
                    defaults={"company_name": ""},
                )
                if created:
                    created_recruiter += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Created {created_seeker} seeker profiles and {created_recruiter} recruiter profiles."
            )
        )