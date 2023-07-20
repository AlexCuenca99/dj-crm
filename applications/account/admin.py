from django.contrib import admin

from .models import CustomUser, Lead, Agent, UserProfile


admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Lead)
admin.site.register(Agent)
