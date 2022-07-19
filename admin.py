from django.contrib import admin

from user.models import login

# Register your models here.
@admin.register(login)
class Batches(admin.ModelAdmin):
    pass
