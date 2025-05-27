from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    return redirect('products:dashboard')

