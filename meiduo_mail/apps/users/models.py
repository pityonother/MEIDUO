from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    mobile=models.CharField(max_length=11,unique=True,vebose_name='手机号')