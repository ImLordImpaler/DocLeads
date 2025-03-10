
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_doctor = models.BooleanField(default=False)
    is_paitent = models.BooleanField(default=False)
    
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_subadmin = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'  # This is what will be used for authentication
    REQUIRED_FIELDS = []  # Other fields required for creating a user

    def __str__(self):
        return "{}-{}".format(self.name, self.phone)


class UserOTP(models.Model):
    phone = models.CharField(max_length=12, unique=True)
    otp = models.CharField(max_length=6, unique=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.phone, self.otp)