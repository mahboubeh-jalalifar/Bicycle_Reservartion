from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import qrcode
from io import BytesIO
from django.core.files import File
from django.core.mail import EmailMessage
import os
from kavenegar import KavenegarAPI

class Bicycle (models.Model):
    user= models.ForeignKey (settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_bicycle") 
    code= models.CharField (max_length=30)
    capacity= models.IntegerField (default=20)
    is_active= models.BooleanField (default=True)
    
    def __str__ (self):
        return f"{self.code} is: {self.is_active}"
    
    @property
    def is_available_count (self):
        return Reservation.objects.filter (bicycle=self, is_active=True).count()
    
    @property
    def available_spot (self):
        return self.capacity - self.is_available_count

class Reservation (models.Model):
    user= models.ForeignKey (settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_reserved")
    bicycle= models.ForeignKey (Bicycle, on_delete=models.CASCADE, related_name="bicycle")
    date = models.DateTimeField (auto_now_add=True)
    is_active= models.BooleanField (default=True)
    qr_code = models.ImageField (upload_to="qr_codes/", blank=True, null=True)

    def __str__ (self):
        return f"{self.user} reserved {self.bicycle} on this day: {self.date}"
    

    def clean (self):
        if self.bicycle.available_spot <= 0 and self.pk is None:
            raise ValidationError ("The reservation for this date is full")
        
    def save (self,*args,**kwargs):
        self.clean ()
        #Gain point
        if self.pk is None:
            super().save(*args,**kwargs)

            self.user.point = getattr (self.user,"point",0) +10
            self.user.save()
            self.bicycle.is_active=False
            self.bicycle.save()
        #Create a QR Code
            qr_data= f"User:{self.user.username}, Bike:{self.bicycle.code} at {self.date}"
            qr_img= qrcode.make (qr_data)
            qr_io= BytesIO()
            qr_img.save(qr_io, format="PNG" ) # type: ignore
            qr_io.seek(0)
            filename= f"qr_{self.user.username}_{self.user.custom_id}.png"
            self.qr_code.save(filename, File(qr_io),save=False)
            super().save(update_fields=["qr_code"],*args,**kwargs)
            
        else:
             super().save(*args,**kwargs)
    
    def delete (self,*args,**kwargs):
        #Decrease the point
            self.user.point = max(0, getattr(self.user,"point", 0) -10)
            self.user.save ()
            self.bicycle.is_active = True
            self.bicycle.save()
            super().delete(*args, **kwargs)

def send_reservation_qrcode_email(self,user, qr_code_path):
        qr_code_path = os.path.join(settings.MEDIA_ROOT, str(self.qr_code))
        if not getattr(user,"email",None):
             raise ValidationError ("Enter Your Email")
        
        subject= "Your Bicycle Rezervation QR Code"
        body= f"Hello {self.user.username},\n\n Your reservation was successful...\n Please take your Qr code"
        email= EmailMessage (subject, body,"your_email@gmail.com",[self.user.email])
        if os.path.exists(qr_code_path):
            email.attach_file(qr_code_path)
            email.send()

def send_sms(self,user,phone, text):
            if not getattr (user,"phone",None):
                 raise ValidationError ("Enter Your PhoneNumber")
            
            api = KavenegarAPI("YOUR_API_KEY")
            text= "Your reservation was successful"
            params = {"sender":phone ,"receptor":self.user.phone,"message":text}
            api.sms_send(params)

   



  