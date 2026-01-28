from django.contrib import admin
from category.models import Category
from django.utils.translation import gettext_lazy as _


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "Parent"]

    def Parent(self, obj):
        return obj.parent.name if obj.parent != None else ""

    Parent.short_description = _("Category__Parent")
