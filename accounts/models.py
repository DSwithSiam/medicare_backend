from datetime import timedelta
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone




class CustomUserManager(UserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=True, is_superuser=True, **extra_fields)
        user.set_password(password)
        user.username = email.split('@')[0]
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    CHOICES_ROLE = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('user', 'User')
    )
    username = models.CharField(max_length=150, unique=True) 
    email = models.EmailField(unique=True)

    role = models.CharField(max_length=20, choices=CHOICES_ROLE, default='user')
    email_verified = models.BooleanField(default=False)
    auth_provider = models.CharField(max_length=50, default='email') 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='users_images/', blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

