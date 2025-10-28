from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import UserModel
from django.utils.translation import gettext_lazy as _ 
from reservation.models import Bicycle,Reservation

class BicycleInLine(admin.StackedInline):
    model=Bicycle
    extra= 0

class ReservationInLine (admin.StackedInline):
    model=Reservation
    extra= 0

@admin.register(UserModel)
class UserModelAdmin (DjangoUserAdmin):
    list_display=("id","email","phone","user_custom_id","role","point","badge","created_date","updated_date","username","date_of_birth","first_name","last_name")
    search_fields=("id","user_custom_id","role","national_id","username","is_available","last_name","first_name")
    list_filter= ("id","user_custom_id","role")
    ordering= ("updated_date","badge")

    fieldsets = (
          (None, {"fields":("username","password")}),
        (_ ("personal information"),{"fields":("first_name","last_name")}),
        (_ ("important_date"),{"fields":("last_login","date_joined")}),
        (_ ("role"),{"fields":("role",)}),
    )
    add_fieldsets = (
        (None, {
            "classes":("wide",),
            "fields":("username","password1","password2","role","first_name","last_name","email","phone"),
        }),
    )
    inlines= [ReservationInLine, BicycleInLine]

