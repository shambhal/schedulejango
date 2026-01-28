from django.db import models


# Create your models here.
class Category(models.Model):
    """
    Category model with hierarchical structure support.
    Categories can have parent categories creating a tree structure.
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_full_path(self):
        """Return the full path of the category including parent categories."""
        path = [self.name]
        parent = self.parent
        while parent:
            path.append(parent.name)
            parent = parent.parent
        return " > ".join(reversed(path))

    def get_descendants(self):
        """Get all descendant categories."""
        descendants = []
        for child in self.children.all():
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants

    def is_root(self):
        """Check if this is a root category (no parent)."""
        return self.parent is None

    def get_level(self):
        """Get the level of this category in the hierarchy."""
        level = 0
        parent = self.parent
        while parent:
            level += 1
            parent = parent.parent
        return level
