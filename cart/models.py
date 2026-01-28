from django.db import models
from doctor.models import Doctor
from django.db.models.fields.related import ForeignKey
# Create your models here.
from django.db import models
from .models import Doctor  # Update this import as per your app structure

class Cart(models.Model):
    dated = models.DateField(blank=False)  # `max_length` is not valid for DateField
    price = models.DecimalField(max_digits=6, decimal_places=2,default=0)  # Removed tuple brackets
    slot = models.CharField(max_length=20)  # `blank=False` is default, can be omitted
    device_id = models.CharField(max_length=50, blank=True)
    user_id = models.IntegerField(blank=True, default=0)  # Consider using ForeignKey to User model
    doctor_id = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        db_column='doctor_id',
        default=0
    )

    def __str__(self):
        return f"{self.dated} - {self.slot} - Doctor {self.doctor_id}"
