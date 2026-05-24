from django.contrib import admin
from .models import Resume, Experience, Education, Skill, Language

admin.site.register(Resume)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(Language)