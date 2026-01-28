from django.contrib import admin
from customer.models import Customer
from django.contrib.admin.options import ModelAdmin
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
  list_display=['name','email']
  def name(self,obj):
    return obj.user.first_name
  def email(self,obj):
    return obj.user.email
  pass
admin.site.register(Customer,CustomerAdmin)    