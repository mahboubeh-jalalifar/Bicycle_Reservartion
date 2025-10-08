from django.contrib import admin
from .models import Reservation,Bicycle

@admin.register(Bicycle)
class BicycleAdmin (admin.ModelAdmin):
    search_fields=["code"]
    list_display=["capacity","is_active"]

@admin.register(Reservation)
class ReservationAdmin (admin.ModelAdmin):
    search_fields=["date","qr_code"]
    list_display= ["is_active","qr_code","date"]
