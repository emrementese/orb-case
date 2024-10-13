from django.contrib import admin
from django.contrib.admin.models import LogEntry

admin.site.site_header = "ORB Admin Portal"
admin.site.site_title = "ORB Admin"
admin.site.index_title = "ORB Root"

admin.site.register(LogEntry)
