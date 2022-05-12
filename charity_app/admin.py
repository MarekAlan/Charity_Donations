from django.contrib import admin

# Register your models here.
from .models import Institution, Donation

admin.site.register(Institution)
admin.site.register(Donation)