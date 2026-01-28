from django.contrib import admin
from django.contrib import admin, messages
from django.shortcuts import render, reverse
from datetime import date
from appoint.utils.dates import Util
from doctor.models import Book,Notification
from doctor.models import Doctor, DoctorSpecial
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .forms import DoctorForm1, DoctorPForm, DoctorTimingsForm
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.conf import settings
from django.urls import path, reverse
import os
from fm.models import ImageTool, FaltuModel as fm2
from django.db import IntegrityError, transaction
from django.utils.html import format_html
import logging


# admin_site = MyAdminSite(name="myadmin")
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    change_form_template = "admin/add_form.html"
    add_form_template = "admin/add_form.html"
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Superusers see everything
        if request.user.is_superuser:
            return qs

        # Doctor sees only their appointments
        try:
            doctor = Doctor.objects.get(user=request.user)
            return qs.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            return qs.none()
        
    def get_urls(self):
        urls = super().get_urls()
        """custom_urls = [
            path('special/<int:size>', self.admin.site.admin_view(self.my_view),name="doctor_special_days")
        ]
        """

        return urls

    list_display = ["Name", "qualification", "writeimage", "department", "specialhours"]

    def specialhours(self, obj):
        return format_html(
            "<a href='../doctorspecial/?doc={}'>{}</a>",
            obj.id,
            obj.name + " Special Days",
        )

    def department(self, obj):
        # print(obj.select_related(categories))

        # print(obj.categories().all())
        cats = obj.categories.all()
        f = ""
        for cat in cats:
            f += cat.name + ","
        return f

    def writeimage(self, obj):
        ffolder = settings.MEDIA_ROOT
        ffolder.replace("\\", "/")
        if not obj.image:
            img = "placeholder.png"

        else:
            img = obj.image

        if os.path.exists(ffolder + img):
            pat = ImageTool.resize(img, 100, 100)
            return format_html("<img src='{}'/>", pat)
        else:
            return ""

    def _update(self, request, object_id, form_url="", extra_context={}):
        # checked

        obj = Doctor.objects.get(pk=object_id)
        img = request.POST["img"]
        pimg = ImageTool.resize("placeholder.png", 100, 100)
        if img != None and img != "":
            thumb = ImageTool.resize(img, 100, 100)
            img = obj.image
        else:
            thumb = ImageTool.resize("placeholder.png", 100, 100)
            img = None
        if obj.id:
            form1 = DoctorForm1(request.POST, instance=obj)
            # form1['first_name']="laila"
            form2 = DoctorPForm(request.POST, instance=obj)
            form3 = DoctorTimingsForm(request.POST, instance=obj)
            extra_context = {
                "form1": form1,
                "form2": form2,
                "form3": form3,
                "pimg": pimg,
            }
            img = request.POST["img"]
            """
                    if(obj.image!=None and obj.image!='') :
                        thumb=ImageTool.resize(obj.image,100,100)
                        img=obj.image
                    else:
                     thumb=ImageTool.resize('placeholder.png',100,100)
                     img=None
                     """

            if form1.is_valid() and form2.is_valid() and form3.is_valid():
                form1.save()
                form2.save()
                form3.save()
                img = request.POST["img"]
                # if(img!=None and img!='') :
                obj.image = img
                obj.save()
                messages.add_message(request, messages.INFO, "Updated Record")
            else:
                print("forms are not valid")
        extra_context["image"] = img
        extra_context["thumb"] = thumb
        extra_context["pimg"] = pimg
        return super().change_view(request, object_id, form_url, extra_context)

    def Name(self, obj):
        return f" {obj.first_name } {obj.last_name} "

    def change_view(self, request, object_id, form_url="", extra_context={}):
        pimg = ImageTool.resize("placeholder.png", 100, 100)
        if request.method == "POST":
            return self._update(request, object_id, form_url, extra_context)
            pass
        else:
            obj = Doctor.objects.get(pk=object_id)
            form1 = DoctorForm1(instance=obj)

            form2 = DoctorPForm(instance=obj)
            form3 = DoctorTimingsForm(instance=obj)
            if obj.image != None and obj.image != "":
                thumb = ImageTool.resize(obj.image, 100, 100)
                img = obj.image
            else:
                thumb = ImageTool.resize("placeholder.png", 100, 100)
                img = None
            extra_context = {
                "pimg": pimg,
                "form1": form1,
                "form2": form2,
                "form3": form3,
                "image": img,
                "thumb": thumb,
            }

            return super().change_view(request, object_id, form_url, extra_context)

    def _save(self, request, form_url="", extra_context={}):
        img = request.POST.get("img", None)
        pimg = ImageTool.resize("placeholder.png", 100, 100)
        if img != None:
            thumb = ImageTool.resize(request.POST["img"], 100, 100)

        else:
            img = None
            thumb = ImageTool.resize("placeholder.png", 100, 100)
        form1 = DoctorForm1(request.POST)
        form2 = DoctorPForm(request.POST)
        form3 = DoctorTimingsForm(request.POST)
        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            email = request.POST["email"]
            User = get_user_model()
            specific_user = User.objects.filter(email=email).exists()
            if specific_user:
                messages.error("Email is not unique")
                extra_content = {
                    "pimg": pimg,
                    "thumb": thumb,
                    "form1": form1,
                    "form2": form2,
                    "form3": form3,
                    "image": img,
                }
                return super().add_view(request, form_url, extra_content)
            arr = request.POST["name"].split(" ")
            last_name = "" if len(arr) < 2 else arr[1]
            first_name = arr[0]
            combined_data = {
                **form1.cleaned_data,
                **form2.cleaned_data,
                **form3.cleaned_data,
            }
            combined_data["first_name"] = first_name
            combined_data["last_name"] = last_name
            combined_data["img"] = img
            del combined_data["name"]
            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                    )
                    doc = Doctor(**combined_data)
                    # doc.save(commit=False)
                    # doc.categories.set([])
                    doc.user = user
                    doc.save()
            except Exception as e:
                messages.error("Error Occured while saving" + e)
                extra_content = {
                    "thumb": thumb,
                    "pimg": pimg,
                    "form1": form1,
                    "form2": form2,
                    "form3": form3,
                    "image": img,
                }
                return super().add_view(request, form_url, extra_content)
            messages.success(request, "Doctor saved successfully")
            return redirect("../doctor/doctor")

    def add_view(self, request, form_url="", extra_context={}):
        if request.method == "POST":
            form1 = DoctorForm1(request.POST)
            form2 = DoctorPForm(request.POST)
            form3 = DoctorTimingsForm(request.POST)
            if request.POST["img"] != None:
                return self._save(request, form_url, extra_content)
            else:
                # when form is not valid
                #
                extra_content = {
                    "thumb": thumb,
                    "form1": form1,
                    "form2": form2,
                    "form3": form3,
                }
                return super().add_view(request, form_url, extra_content)
        else:
            form1 = DoctorForm1()
            form2 = DoctorPForm()
            form3 = DoctorTimingsForm()

        extra_context["form1"] = form1
        extra_context["form2"] = form2
        thumb = ImageTool.resize("placeholder.png", 100, 100)
        extra_content = {
            #'furl':furl,
            "form3": form3,
            "thumb": thumb,
            "img": None,
            "form1": form1,
            "form2": form2,
        }
        return super().add_view(request, form_url, extra_content)

    def get_urls(self):
        urls = super().get_urls()

        # urls.remove(urls[1])
        """
       # view_name = 'whrs_add'
        my_urls= [
            path('reschedule/<int:bookid>',self.admin_site.admin_view(self.reschedule),name="reschedule_appointment"),
            path('appointhistory/<int:bookid>',self.admin_site.admin_view(self.appointhistory),name="appointmenthistory"),
        ]
       
        #print(my_urls);
        #return urls
        return urls+my_urls
        """
        return urls


admin.site.register(Doctor, DoctorAdmin)


class DoctorFilter(admin.SimpleListFilter):
    title = "Doctor"
    parameter_name = "doc"

    def lookups(self, request, model_admin):
        arr = []
        records = Doctor.objects.order_by("first_name", "last_name").all()
        for record in records:
            arr.append((record.id, record.first_name + " " + record.last_name))

        return arr

    def queryset(self, request, queryset):
        val = self.value()
        # us=Doctor.objects.get(pk=val)
        if val:
            return queryset.filter(doctor__id=val)  # ✅ correct field lookup
        return queryset


class MonthFilter(admin.SimpleListFilter):
    title = _("Month")  # Human-readable title
    parameter_name = "month"  # URL parameter name

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each tuple is the coded value
        for the option that will appear in the URL query. The second element is the
        human-readable name for the option that will appear in the right sidebar.
        """
        return [
            (1, _("January")),
            (2, _("February")),
            (3, _("March")),
            (4, _("April")),
            (5, _("May")),
            (6, _("June")),
            (7, _("July")),
            (8, _("August")),
            (9, _("September")),
            (10, _("October")),
            (11, _("November")),
            (12, _("December")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            month = int(self.value())
            year = date.today().year  # or any fixed year you want
            start = date(year, month, 1)

            # Handle month-end correctly
            if month == 12:
                end = date(year + 1, 1, 1)
            else:
                end = date(year, month + 1, 1)

            return queryset.filter(
                sdate__gte=start, sdate__lt=end
            )  # 'sdate' is your date field
        return queryset


class DoctorSpecialAdmin(admin.ModelAdmin):
    # list_filter=['doctor__first_name','doctor__id']
    def get_readonly_fields(self, request, obj=None):
        if obj:  # obj is not None => change view
            return ["doctor_id"]  # or return super() + ['email']
        return []  # add view — all fields editable

    list_display = ["id", "doctor_id", "sdate", "month_display"]
    list_filter = [DoctorFilter, MonthFilter]

    def month_display(self, obj):
        if obj.sdate:
            return obj.sdate.strftime("%B")  # 'June'
        return "-"

    month_display.short_description = "Month"
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
       def send_notification_bulk(self, request, queryset):
            count = 0
            for book in queryset:
                if book.status in ["BOOKED", "CANCELLED"]:
                    # your notification logic
                   
                    Notification.objects.create(book=book, type='mail')
                    count += 1

            self.message_user(
                request,
                f"Notification sent for {count} bookings",
                messages.SUCCESS
            )

       send_notification_bulk.short_description = "Send notification to selected bookings"
       def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "send-notification/<int:book_id>/",
                self.admin_site.admin_view(self.create_notification),
                name="book-send-notification",
            ),
        ]
        return custom_urls + urls
       actions = ["send_notification_bulk"]
       def slots(self,object):
           return Util.to_ampm(object.slot)
       def trigger_email(self,bookid):
           bk=Book.objects.get(id==bookid)
           if(bk.exists()):
              pass
       def send_notification(self, obj):
        if obj.status in ["BOOKED", "CANCELLED"]:
            return format_html(
                '<a class="button" href="{}">Send Notification</a>',
                f"send-notification/{obj.id}/"
            )
        return "-"
       send_notification.short_description = "Notification"
       def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Superusers see everything
        if request.user.is_superuser:
            return qs

        # Doctor sees only their appointments
        try:
            doctor =Doctor.objects.get(user=request.user)
            return qs.filter(doctor_id_id=doctor.id)
        except Doctor.DoesNotExist:
            return qs.none()
        
       def create_notification(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            messages.error(request, "Book not found")
            return redirect(request.META.get("HTTP_REFERER"))

        # ✅ Your notification logic here
        # Example:
        # send_mail(...)
        Notification.objects.create(book=book, type='mail')

        messages.success(
            request,
            f"Notification sent for booking #{book.id}"
        )
        return redirect(request.META.get("HTTP_REFERER"))
       def doctor_first_name(self, obj):
        return obj.doctor_id.first_name
       doctor_first_name.short_description = "Doctor Name"
       list_display = ["slots", "status","dated",'doctor_first_name','send_notification']
admin.site.register(DoctorSpecial, DoctorSpecialAdmin)
