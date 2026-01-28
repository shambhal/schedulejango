from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import request
from django.http import HttpRequest,HttpResponse
# Create your views here.
def test(request):
   user = authenticate(username='admin', password='123456')
   print(user) 
   return HttpResponse("KUCHKIKO")
