from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

# Create your views here.
def get_home(request):
    return render(request, 'Home.html')
