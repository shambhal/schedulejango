from django.db import models
from category.models import Category
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User
from doctor.constants import SERVICE_STATUS
from django.db.models.fields.related import ForeignKey
from django.db.models import Q, UniqueConstraint
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
# Create your models here.

class Doctor(models.Model):

    """
    Doctor model that can be associated with multiple categories.
    """

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    # date_of_birth = models.DateField(blank=True, null=True)
    @property
    def name(self):
        return self.first_name + " " + self.last_name

    sunday = models.TextField(blank=False, default="00:00-00:00#0")
    monday = models.TextField(blank=False, default="10:00-18:00#500")
    tuesday = models.TextField(blank=False, default="10:00-18:00#500")
    wednesday = models.TextField(blank=False, default="10:00-18:00#500")
    thursday = models.TextField(blank=False, default="10:00-18:00#500")
    friday = models.TextField(blank=False, default="10:00-18:00#500")
    saturday = models.TextField(blank=False, default="00:00-00:00#0")
    slot = models.IntegerField(
        blank=False, default=1800, help_text="Session in seconds"
    )

    off = models.TextField(blank=True)

    # Professional information
    license_number = models.CharField(max_length=50, default="abcde83939")
    specialization = models.CharField(max_length=100, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    qualification = models.TextField(blank=True)
    
    # Contact information
    # address = models.TextField(blank=True)
    # city = models.CharField(max_length=50, blank=True)
    # state = models.CharField(max_length=50, blank=True)
    # zip_code = models.CharField(max_length=10, blank=True)
    # country = models.CharField(max_length=50, default='India')
    image = models.CharField(max_length=100, default="", blank=True)

    # Professional details
    # hospital_affiliation = models.CharField(max_length=100, blank=True)
    # min_consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True,default=400)
    bio = models.TextField(blank=True)

    # Many-to-many relationship with categories

    categories = models.ManyToManyField(
        Category, through="DoctorCategory", related_name="doctors"
    )

    # Status and timestamps
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        """
        indexes = [
        models.Index(fields=['email'], name='doctor_email_idx'),
        models.Index(fields=['license_number'], name='doctor_license_idx'),
         ]
        """

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_primary_category(self):
        """Get the primary category for this doctor."""
        primary_relation = self.doctorcategory_set.filter(is_primary=True).first()
        return primary_relation.category if primary_relation else None


class DoctorCategory(models.Model):
    """
    Through model for Doctor-Category relationship with additional fields.
    """

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)
    expertise_level = models.CharField(
        max_length=20,
        choices=[
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
            ("advanced", "Advanced"),
            ("expert", "Expert"),
        ],
        default="intermediate",
    )
    years_in_category = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("doctor", "category")
        verbose_name = "Doctor_Category"
        verbose_name_plural = "Doctor_Categories"

    def __str__(self):
        return f"{self.doctor} - {self.category}"


# Optional: Model for category-specific doctor ratings


class DoctorCategoryRating(models.Model):
    """
    Rating model for doctors in specific categories.
    """

    doctor_category = models.ForeignKey(DoctorCategory, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],  # 1-5 stars
        help_text="Rating from 1 to 5 stars",
    )
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("doctor_category", "patient")
        verbose_name = "Doctor Category Rating"
        verbose_name_plural = "Doctor Category Ratings"

    def __str__(self):
        return f"{self.doctor_category} - {self.rating} stars"


class DoctorSpecial(models.Model):
    class Meta:
        verbose_name = "Doctor Special Day Timings"
        verbose_name_plural = "Doctor Special Days"

    def __str__(self) -> str:
        # return self.sdate +self.service.name
        return self.doctor.name + " " + str(self.sdate)

    # sdate=models.DateField('Special Date')
    sdate = models.DateField()

    hours = models.TextField(blank=False, default="08:00-12:00")
    off = models.TextField(blank=True)
    doctor = ForeignKey(Doctor, related_name="doctor", on_delete=models.CASCADE)


class Book(models.Model):
    # st=[('UN','UNAVAILABLE'),('AV','AVAILABLE')]
    def __str__(self) -> str:
        return self.name + "-" + str(self.dated) + "-" + self.slot

    dated = models.DateField(blank=False, max_length=20)
    doctor_id = ForeignKey(Doctor, on_delete=models.CASCADE, default=1,db_column='doctor_id')
    slot = models.CharField(blank=False, max_length=20)
    desc = models.TextField(
        blank=True,
    )
    name = models.CharField(blank=False, max_length=60)
    phone = models.CharField(max_length=15)
    order_id = models.IntegerField(blank=True, default=0)
    email = models.CharField(max_length=150, blank=True, default="demo@gmail.com")
    status = models.CharField(choices=SERVICE_STATUS, max_length=15, default="AV")
    device_id = models.CharField(blank=True, max_length=150)
    user_id = models.IntegerField(blank=True, default=0)
    order_item_id = models.IntegerField(blank=True, default=0)
    extra_info = models.TextField(blank=True, default="")

    class Meta:
        constraints = [
            UniqueConstraint(
                condition=Q(status="BOOKED"),
                fields=["dated", "doctor_id", "slot"], name="unique2_booking"
            )
        ]
class BookHistory(models.Model):
    dated = models.DateField(blank=False, max_length=20, default=timezone.now)
    status = models.CharField(max_length=20, blank=False)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    info = models.TextField(blank=True)
class Notification(models.Model):
    book=models.OneToOneField(Book,on_delete=models.CASCADE)  
    type=models.CharField(max_length=5    ) 
    created_at = models.DateTimeField(auto_now_add=True)
    @classmethod
    def can_create(cls, book, type):
        five_minutes_ago = timezone.now() - timedelta(minutes=5)

        return not cls.objects.filter(
            book=book,
            type=type,
            created_at__gte=five_minutes_ago
        ).exists()
    def save(self, *args, **kwargs):
        if not self.pk:
            five_minutes_ago = timezone.now() - timedelta(minutes=5)

            exists = Notification.objects.filter(
                book=self.book,
                type=self.type,
                created_at__gte=five_minutes_ago
            ).exists()

            if exists:
                raise ValidationError("Notification already sent within last 5 minutes")

        super().save(*args, **kwargs)