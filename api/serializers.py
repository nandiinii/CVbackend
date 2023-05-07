from rest_framework import serializers
from .models import User, ApplicantDetails,DetailAdd
from rest_framework.permissions import IsAuthenticated

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68,min_length=6,write_only=True)
    permission_classes=[IsAuthenticated]
    class Meta:
        model=User
        fields=['email','username','password']

    def validate(self,attrs):
        email=attrs.get('email','')
        username=attrs.get('username','')

        if not username.isalnum():
            raise serializers.ValidationError("username should contain only alpha numeric chars")
        return attrs

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email']

class ApplicantDetailsSerializer(serializers.ModelSerializer):
    def validate(self,data):
        Name=data['Name']
        DOB=data['DOB']
        Location=data['Location']
        Gender=data['Gender']
        JobRole=data['JobRole']
        PhoneNo=data['PhoneNo']
        EmailID=data['EmailID']
        LinkedIn=data['LinkedIn']
        return data
    
    class Meta:
        model=ApplicantDetails
        fields='__all__'


class DetailAddSerializer(serializers.ModelSerializer):
    class Meta:
        model=DetailAdd
        fields=['name','dob','location','gender']
    
    