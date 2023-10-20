from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','password','firstname','lastname']
        
        extra_kwargs={
            'email': {'error_messages': {'required': "email is required",'blank':'please provide a email'}},
            'password': {'error_messages': {'required': "password is required",'blank':'please Enter a password'}},
            'firstname': {'error_messages': {'required': "firstname is required",'blank':'firstname could not blank'}},
            'lastname': {'error_messages': {'required': "lastname is required",'blank':'lastname could not blank'}},
        }
        
        
    def create(self,validate_data,):
        user=User.objects.create(
            email=validate_data['email'],
            firstname=validate_data['firstname'],
            lastname=validate_data['lastname'],
        )
        
        user.set_password(validate_data['password'])
        user.save()
        return user
    
    
class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model =User
        fields=['email','password']
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','firstname','lastname']
        
        
class FileDataSerializer(serializers.ModelSerializer):
    class Meta:
        model= FileData
        fields = '__all__'
           
    def create(self, validate_data):
        return User_PDF.objects.create(**validate_data)