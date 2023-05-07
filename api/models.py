from django.db import models
from email.policy import default
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin,User)
from django.core.validators import FileExtensionValidator
import uuid

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
        # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applicant_details', default=None)
        PhoneNo=models.CharField(blank=False,max_length=10)
        EmailID=models.EmailField(blank=False,max_length=254)
        LinkedIn=models.CharField(blank=False, max_length=100)
        ResumeFile=models.FileField(upload_to="", validators = [FileExtensionValidator(allowed_extensions=['pdf'])])

        def __str__(self):
          return self.LinkedIn

class DetailAdd(models.Model):
     #id = models.AutoField(primary_key=True)
     name=models.CharField(max_length=25,blank=False)
     dob=models.DateField()
     location=models.CharField(max_length=25)
     GENDER_CHOICES=(
        ('Male','Male'),
        ('Female','Female'), )
     gender=models.CharField(max_length=6,choices=GENDER_CHOICES)
     def _str_(self):
        return self.name

class DetailAddtwo(models.Model):
    mailid = models.CharField(max_length=25)
    phoneno = models.CharField(max_length=10)
    linked_in_url = models.URLField(max_length=50)
    job_role = models.CharField(max_length=20)
    resume = models.FileField(upload_to='',validators = [FileExtensionValidator(allowed_extensions=['pdf'])])
    img = models.ImageField(upload_to='images',blank=True,null=True)

    def __str__(self):
        return self.mailid
