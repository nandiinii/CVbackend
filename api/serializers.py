from rest_framework import serializers
from .models import User, DetailAddtwo,DetailAdd
from rest_framework.permissions import IsAuthenticated
from django.core.validators import FileExtensionValidator

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

class DetailAddSerializer(serializers.ModelSerializer):
    class Meta:
        model=DetailAdd
        fields=['id','name','location','dob','gender']
        #fields='__all__'       

class DetailAddTwoSerializer(serializers.ModelSerializer):
    resume = serializers.FileField(validators = [FileExtensionValidator(allowed_extensions=['pdf'])])
    class Meta:
        model = DetailAddtwo
        fields='__all__'
    def to_representation(self, instance):
        if isinstance(instance, DetailAddtwo):
            return {
                'mailid': instance.mailid,
                'phoneno': instance.phoneno,
                'linked_in_url': instance.linked_in_url,
                'resume': instance.resume.url if instance.resume else None,
                'img': instance.img.url if instance.img else None
            }
        else:
            return instance


        