from django.contrib import admin
from aushadha_users.models import AuShadhaUser


class AuShadhaUserInline(admin.StackedInline):
    model = AuShadhaUser      



"""
AuShadhaUser Admin
"""
class AuShadhaUserAdmin(admin.ModelAdmin):
    inlines = [ AuShadhaUserInline ]
    extra = 0

    

admin.site.register(AuShadhaUser, AuShadhaUserAdmin)

