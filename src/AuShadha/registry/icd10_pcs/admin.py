from registry.icd10_pcs.models import RootXML, PcsTable, PcsRow, Axis, Label, Title, Definition

from django.contrib import admin


class RootXMLAdmin(admin.ModelAdmin):
    pass


class PcsTableAdmin(admin.ModelAdmin):
    pass


class PcsRowAdmin(admin.ModelAdmin):
    pass


class AxisAdmin(admin.ModelAdmin):
    pass


class TitleAdmin(admin.ModelAdmin):
    pass


class LabelAdmin(admin.ModelAdmin):
    pass


class DefinitionAdmin(admin.ModelAdmin):
    pass


admin.site.register(RootXML, RootXMLAdmin)
admin.site.register(PcsTable, PcsTableAdmin)
admin.site.register(PcsRow, PcsRowAdmin)
admin.site.register(Axis, AxisAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Definition, DefinitionAdmin)
