from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator

  
class Interest(models.Model):
    name = models.CharField(max_length=200,blank=False,null=False,unique=True)

    def __str__(self):
        return self.name[:20]


class User(AbstractUser):
    username_regex = RegexValidator(regex=r"^(?=.*[a-z])[a-z\d]{5,}$", message="Please enter small case letters and required username must have 5 letters at least")
    username = models.CharField(max_length=50, unique=True,validators=[username_regex])
    fullname = models.CharField(max_length=200,blank=False,null=False)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Please enter a valid 10 digit phone number")
    phone = models.CharField(max_length=20,unique=True,validators=[phone_regex])
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    country = models.CharField(max_length=100)
    online = models.BooleanField(default=False)
    Interest_CHOICES = [
        ('Food', 'Food'),
        ('Movies', 'Movies'),
        ('Travel', 'Travel'),
        ('Cycling', 'Cycling'),
    ]
    #interests =  models.CharField(max_length=20,null=True,choices=Interest_CHOICES)
    interests =  models.ManyToManyField('Interest')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone', 'gender', 'country','username']

    def make_password(self,password):
        self.password = make_password(password)
