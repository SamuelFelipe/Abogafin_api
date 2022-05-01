from django.contrib import admin

from califications.models import LawFirmCalification, UserCalification

admin.site.register(UserCalification)
admin.site.register(LawFirmCalification)
