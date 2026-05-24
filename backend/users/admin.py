from django.contrib import admin
from .models import User, SeekerProfile, RecruiterProfile

admin.site.register(User)
admin.site.register(SeekerProfile)
admin.site.register(RecruiterProfile)