from django.db import models
from doctor.models import Doctor
from doctor.constants import SERVICE_STATUS
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.db.models import UniqueConstraint
# Create your models here.



from django.db import models
from django.conf import settings

# Assuming you already have a Category model in, say, `shop.models`
# Adjust the import accordingly
from  category.models import Category  

'''
class Banner(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="banners"
    )
    image = models.ImageField(upload_to="banners/")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return f"Banner for {self.category.name} (order {self.sort_order})"
'''