from django.contrib import admin

from .models import CustomUser, Agent, UserProfile


admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Agent)
