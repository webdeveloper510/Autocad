from django.db import models
from django.contrib.auth.models import *

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,firstname,lastname,password=None):
        if not email:
            raise ValueError("user must have an email address")
        
        user=self.model(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None):
        user=self.create_user(
            email,
            firstname="None",
            lastname="None",
            password=password,
        )
        user.is_admin=True
        user.save(using=self._db)
        return user
    
# Custom user Model

class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(
        verbose_name='email_address',
        max_length=225,
        unique=True
    )
    
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateField(auto_now=True)
    
    
    objects=UserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    
    def ___str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin


    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
    
    
    
class FileData(models.Model):
    stpfile=models.FileField(upload_to="stp_file/",blank=True,null=True)
    filename=models.CharField(max_length=200,blank=True,null=True)
    pdffile=models.CharField(max_length=200,blank=True,null=True)
    
    