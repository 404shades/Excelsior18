from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, mobile_no, roll_no, password=None, is_staff=False, is_admin=False, active=True):
        if not email:
            raise ValueError("Users Must have an email address")
        if not password:
            raise ValueError("Password is required")
        if not mobile_no:
            raise ValueError('User Must Provide their Mobile Number For Verification')
        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            mobile_no=mobile_no,
            roll_no=roll_no,

        )
        user_obj.set_password(password)
        user_obj.active= active
        user_obj.staff=is_staff
        user_obj.admin=is_admin
        user_obj.save(using=self.db)
        return user_obj

    def create_superuser(self, email, full_name, mobile_no, password=None, roll_no=None):
        user = self.create_user(
            email,
            full_name,
            mobile_no,
            password=password,
            roll_no=roll_no,
            is_staff=True,
            is_admin=True
        )
        return user

    def create_staffuser(self, email, full_name, mobile_no, password=None, roll_no=None):
        user = self.create_user(
            email,
            full_name,
            mobile_no,
            password=password,
            is_staff=True,
            roll_no=roll_no,
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    full_name =  models.CharField(max_length=255)
    mobile_no = PhoneNumberField(null=True, blank=True)
    roll_no = models.CharField(null=True, blank=True, max_length=15)
    # mobile_no = PhoneNumberField()
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin  = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'mobile_no', 'roll_no']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def get_mobile(self):
        if self.mobile_no:
            return self.mobile_no
        return None

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


