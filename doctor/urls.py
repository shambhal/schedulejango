from django.contrib import admin
from django.urls import path, include

from doctor import views

app_name = "doctor"
urlpatterns = [
    path("test/", views.test, name="doctor-test"),

]