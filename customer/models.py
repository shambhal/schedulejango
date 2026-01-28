from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    user = models.OneToOneField(User, on_delete=models.CASCADE, default="shambhal")
    phone = models.CharField(null=True, blank=True, max_length=20)
    access = models.CharField(null=True, max_length=150)
    refresh = models.CharField(null=True, max_length=150)