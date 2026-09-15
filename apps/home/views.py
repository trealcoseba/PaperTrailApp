from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect

@login_required
def home_view(request):
    return render(request, "home/home.html")

def logout_view(request):
    logout(request)
    return redirect("login:login")