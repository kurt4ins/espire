from django.contrib import admin
from userapp.models import EmailVerification

# Register your models here.

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("key", "user", "experation")
    fields = ("key", "user", "created", "experation")
    readonly_fields = ("created",)