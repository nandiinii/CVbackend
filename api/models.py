from django.db import models
from email.policy import default
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if username is None:
            raise TypeError("Users should have a username")

        if email is None:
            raise TypeError("Users should have a email")

        user=self.model(username=username,email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,email,password=None):
        if password is None:
            raise TypeError("Password should not be none")
        
        user=self.create_user(username,email,password)
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(max_length=255,unique=True,db_index=True)
    email=models.EmailField(max_length=255,unique=True,db_index=True)
    is_verified=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    objects=UserManager()
    def __str__(self):
        return self.username

    def tokens(self):
        return ''

    
class ApplicantDetails(models.Model):
        Name=models.CharField(blank=False, max_length=50)
        DOB=models.DateField(blank=False,auto_now=False, auto_now_add=False)
        Location=models.CharField(blank=False, max_length=50)
        JobRole=models.CharField( blank=False,max_length=50)
        GENDER_CHOICES=(
             ('Male','Male'),
             ('Female','Female'),
             ('Others','Others')
        )
        Gender=models.CharField(blank=False,max_length=6, choices=GENDER_CHOICES)
        PhoneNo=models.CharField(blank=False,max_length=10)
        EmailID=models.EmailField(blank=False,max_length=254)
        LinkedIn=models.CharField(blank=False, max_length=100)
        ResumeFile=models.FileField(upload_to="", max_length=100)
        def __str__(self):
          return self.Name