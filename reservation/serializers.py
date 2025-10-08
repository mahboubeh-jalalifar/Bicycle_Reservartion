from rest_framework import serializers
from .models import Bicycle, Reservation
from accounts.serializers import UserSerializer
from rest_framework.exceptions import ValidationError

class BicycleSerializer (serializers.ModelSerializer):
    class Meta:
        model = Bicycle
        fields= ["code","is_active","capacity"]
        read_only_fields= ["code","is_active"]

class ReservationSerializer (serializers.ModelSerializer):
    bicycle = BicycleSerializer (read_only=True)
    bicycle_id = serializers.IntegerField(write_only=True)
    qr_code_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model= Reservation
        fields= ["user","bicycle","date","is_active","user_custom_id","bicycle_id","qr_code","qr_code_url"]
        read_only_fields= ["qr_code_urld"]

    def get_qr_code_url(self,obj):
        if obj.qr_code:
            return obj.qr_code.url
        return None
            
    def validate (self,data):
        bicycle_id = data.get("bicycle_id")
        try :
            bicycle = Bicycle.objects.get (id=bicycle_id)
        except Bicycle.DoesNotExist:
            raise serializers.ValidationError ("Bicycle does not found")
        if bicycle.available_spot<=0:
            raise serializers.ValidationError ("This bicycle is already reserved")
        
        user_custom_id= data.get ("user_custom_id") or self.context["request"].user.custom_id
        if Reservation.objects.filter (user_custom_id= user_custom_id, bicycle=bicycle, is_active=True).exists():
            raise serializers.ValidationError ("You reserved it")
        
        return data
        
    def create (self,validated_data):
        user_custom_id = validated_data.pop ("user_custom_id")
        bicycle = Bicycle.objects.get (id = validated_data.pop ("bicycle_id"))
        user= self.context["request"].user    
        reservation = Reservation.objects.create (
            user=user,user_custom_id=user_custom_id,bicycle=bicycle,**validated_data)
        return reservation

