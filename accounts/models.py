from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid
from django.utils.timezone import now

class Roles (models.TextChoices):
    User = "User", "User"
    Employee= "Empolyee" , "Employee"
    Admin = "Admin" , "Admin"
    Manager = "Manager" , "Manager"
    Others = "Others", "Others"

class Gender (models.TextChoices):
    Male= "Male","Male",
    Female= "Female","Female",
    Other= "Other","Other",


class UserModel (AbstractUser):
    email = models.EmailField (max_length=50, unique=True)
    phone = models.IntegerField (help_text="+989", null=True, blank=True)
    city = models.CharField (max_length=30)
    province = models.CharField (max_length=30, null=True, blank=True)
    role = models.CharField (max_length=20, choices=Roles.choices , default=Roles.User)
    national_id = models.IntegerField (help_text="2580945710", null=True, blank=True)
    date_of_birth = models.DateField (help_text="YYYY/MM/DD", null=True, blank=True)
    gender = models.CharField (max_length=20, choices=Gender.choices , default=Gender.Other)
    point = models.IntegerField (default=0)
    created_date = models.DateTimeField (auto_now_add=True)
    updated_date = models.DateTimeField (auto_now=True)
    custom_id = models.CharField (max_length= 50, unique=True)
    is_avaiable= models.BooleanField(default=True)
    badge= models.CharField (max_length=50, default="Beginner", blank=True)
    
    def update_badge(self):
        if self.point <=50:
            self.badge ="Begginer"
        elif self.point <=100:
            self.badge ="Active Rider"
        elif self.point <= 200 :
            self.badge ="Pro Cyclist"
        else:
            self.badge ="VIP Gold"
    
    def save (self,*args,**kwargs):
        if not self.custom_id:
            year= now().year
            letter= self.username[:3].upper ()
            uuid_num= str(uuid.uuid4().int)[:6]
            self.custom_id= f"{letter}{year}{uuid_num}"
        super().save(*args,**kwargs)
        
    def __str__ (self):
        return self.username 

