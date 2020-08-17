from django.contrib import admin
from .models import Committee


class CommitteeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "date_created",
        "date_updated",
        "author",
    )
    search_fields = (
        "name",
        "author",
    )
    readonly_fields = ("date_created", "date_updated")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Committee, CommitteeAdmin)
