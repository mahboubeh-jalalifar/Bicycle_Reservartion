from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserModel

User= get_user_model ()

class UserSerializer (serializers.ModelSerializer):
    password= serializers.CharField (write_only= True)
    class Meta:
        model= UserModel
        fields= ["username","password","email","phone","city","province","role","national_id","date_of_birth","gender","point","created_date","updated_date","custom_id","badge"]
        read_only_fields= ["custom_id"]

    def create (self,validated_data):
        password = validated_data.pop ("password")
        user = User  (**validated_data)
        validate_password (password,user)
        user.set_password (password)
        user.save ()
        return user 
    
    def update (self,instance,validated_data):
        password= validated_data.pop ("password", None)
        for key, value in validated_data.itmes():
            setattr (instance,key,value)
            if password:
                validate_password(password, instance)
                instance.set_password (password)
            instance.save()
            return instance 

