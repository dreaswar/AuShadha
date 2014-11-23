from django.contrib import admin
from history.social_history.models import SocialHistory


class SocialHistoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(SocialHistory, SocialHistoryAdmin)
