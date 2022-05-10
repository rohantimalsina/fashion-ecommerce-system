from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ContactUs(models.Model):
    name=models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()


    class Meta:
        verbose_name_plural='ContactUs'