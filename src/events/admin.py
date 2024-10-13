from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventsModelAdmin(admin.ModelAdmin):
    list_display = ["__str__", "title", "date", "is_deleted"]
    search_fields = ["id", "title"]
