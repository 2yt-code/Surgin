from django.contrib import admin

from apps.api.v1.account.models import (
    Device, 
    FingerPrint,
    Membership, 
    UserPreferences
)


admin.site.register(Membership)
admin.site.register(Device)
admin.site.register(FingerPrint)
admin.site.register(UserPreferences)