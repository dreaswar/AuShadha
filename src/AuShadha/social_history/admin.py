from django.contrib import admin
from social_history.models import SocialHistory


class SocialHistoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(SocialHistory, SocialHistoryAdmin)
