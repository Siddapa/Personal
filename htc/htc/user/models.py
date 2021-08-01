from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self, first, last, email, phone, bio, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            first = first,
            last = last,
            email = self.normalize_email(email),
            phone = phone,
            rating = 0,
            bio = bio
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first, last, email, phone, password):
        user = self.create_user(
            first = first,
            last = last,
            email = self.normalize_email(email),
            phone = phone,
            rating = 0,
            bio = "",
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()


class User(AbstractBaseUser):
    # User data
    first = models.CharField(max_length=50)
    last = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)
    rating = models.IntegerField(default=0) # Needs to be restricted from 1-5 within form
    bio = models.CharField(max_length=1000)

    # Admin stuff
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first', 'last', 'phone', 'password']

    objects = AccountManager()

    def __str__(self):
        return f"{self.first} {self.last}"
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True