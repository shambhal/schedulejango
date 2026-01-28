from django.db import models

# Create your models here.
from  category.models import Category  


class Banner(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="banners"
    )
    image = models.CharField(max_length=100, default="", blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    tag=models.CharField(max_length=5,blank=True)
    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return f"Banner for {self.category.name} (order {self.sort_order})"
