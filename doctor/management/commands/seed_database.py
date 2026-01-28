# management/commands/seed_database.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from category.models import Category
from doctor.models import Doctor, DoctorCategory
from django.db import transaction
import json


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding",
        )
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Number of doctors to create",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing data..."))
            self.clear_data()

        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))

        with transaction.atomic():
            categories = self.create_categories()
            users = self.create_users(options["count"])
            doctors = self.create_doctors(users, categories)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded database with {len(doctors)} doctors"
            )
        )

    def clear_data(self):
        """Clear existing data"""
        Doctor.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

    def create_categories(self):
        """Create medical categories with hierarchy"""
        categories_data = [
            # Root categories
            {"name": "General Medicine", "slug": "general-medicine", "parent": None},
            {"name": "Surgery", "slug": "surgery", "parent": None},
            {"name": "Pediatrics", "slug": "pediatrics", "parent": None},
            {"name": "Cardiology", "slug": "cardiology", "parent": None},
            {"name": "Dermatology", "slug": "dermatology", "parent": None},
            # Sub-categories
            {"name": "Cardiac Surgery", "slug": "cardiac-surgery", "parent": "Surgery"},
            {"name": "Plastic Surgery", "slug": "plastic-surgery", "parent": "Surgery"},
            {
                "name": "Pediatric Cardiology",
                "slug": "pediatric-cardiology",
                "parent": "Cardiology",
            },
            {
                "name": "Interventional Cardiology",
                "slug": "interventional-cardiology",
                "parent": "Cardiology",
            },
            {"name": "Neonatal Care", "slug": "neonatal-care", "parent": "Pediatrics"},
        ]

        categories = {}

        # Create root categories first
        for cat_data in categories_data:
            if cat_data["parent"] is None:
                category = Category.objects.create(
                    name=cat_data["name"],
                    slug=cat_data["slug"],
                    description=f"Medical specialty in {cat_data['name']}",
                )
                categories[cat_data["name"]] = category
                self.stdout.write(f"Created category: {category.name}")

        # Create sub-categories
        for cat_data in categories_data:
            if cat_data["parent"] is not None:
                parent_category = categories[cat_data["parent"]]
                category = Category.objects.create(
                    name=cat_data["name"],
                    slug=cat_data["slug"],
                    parent=parent_category,
                    description=f"Subspecialty in {cat_data['name']}",
                )
                categories[cat_data["name"]] = category
                self.stdout.write(f"Created subcategory: {category.name}")

        return categories

    def create_users(self, count):
        """Create user accounts for doctors"""
        users = []
        for i in range(count):
            username = f"doctor{i+1}"
            email = f"doctor{i+1}@hospital.com"

            user = User.objects.create_user(
                username=username,
                email=email,
                password="password123",
                first_name=f"Doctor{i+1}",
                last_name=f"LastName{i+1}",
            )
            users.append(user)

        self.stdout.write(f"Created {len(users)} users")
        return users

    def create_doctors(self, users, categories):
        """Create doctor profiles"""
        doctors = []
        specializations = [
            "Internal Medicine",
            "Cardiology",
            "Pediatrics",
            "Surgery",
            "Dermatology",
            "Neurology",
            "Orthopedics",
        ]

        cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad"]

        category_list = list(categories.values())

        for i, user in enumerate(users):
            doctor = Doctor.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone=f"+91-{9000000000 + i}",
                gender="M" if i % 2 == 0 else "F",
                license_number=f"MED{10000 + i}",
                specialization=specializations[i % len(specializations)],
                years_of_experience=(i % 20) + 1,
                qualification=f"MBBS, MD in {specializations[i % len(specializations)]}",
                address=f"Hospital Address {i+1}",
                city=cities[i % len(cities)],
                state="Maharashtra"
                if cities[i % len(cities)] == "Mumbai"
                else "Karnataka",
                zip_code=f"{400000 + i}",
                hospital_affiliation=f"City Hospital {i+1}",
                min_consultation_fee=500 + (i * 100),
                bio=f"Experienced doctor specializing in {specializations[i % len(specializations)]}",
                is_verified=True,
            )

            # Assign categories to doctors
            primary_category = category_list[i % len(category_list)]
            DoctorCategory.objects.create(
                doctor=doctor,
                category=primary_category,
                is_primary=True,
                expertise_level="expert" if i % 4 == 0 else "advanced",
                years_in_category=(i % 15) + 1,
            )

            # Add secondary category for some doctors
            if i % 3 == 0 and len(category_list) > 1:
                secondary_category = category_list[(i + 1) % len(category_list)]
                if secondary_category != primary_category:
                    DoctorCategory.objects.create(
                        doctor=doctor,
                        category=secondary_category,
                        is_primary=False,
                        expertise_level="intermediate",
                        years_in_category=(i % 10) + 1,
                    )

            doctors.append(doctor)
            self.stdout.write(f"Created doctor: {doctor}")

        return doctors


# Alternative: Simple seeding script
# management/commands/simple_seed.py
class SimpleCommand(BaseCommand):
    help = "Simple database seeding"

    def handle(self, *args, **options):
        # Create a superuser
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin", email="admin@hospital.com", password="admin123"
            )
            self.stdout.write("Created superuser: admin")

        # Create basic categories
        categories = [
            "General Medicine",
            "Cardiology",
            "Pediatrics",
            "Surgery",
            "Dermatology",
        ]

        for cat_name in categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={
                    "slug": cat_name.lower().replace(" ", "-"),
                    "description": f"Medical specialty in {cat_name}",
                },
            )
            if created:
                self.stdout.write(f"Created category: {cat_name}")

        self.stdout.write(self.style.SUCCESS("Database seeding completed!"))
