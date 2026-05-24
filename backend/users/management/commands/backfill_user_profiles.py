from django.core.management.base import BaseCommand

from users.models import RecruiterProfile, SeekerProfile, User


class Command(BaseCommand):
    help = "Create missing seeker/recruiter profiles for existing users."

    def handle(self, *args, **options):
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