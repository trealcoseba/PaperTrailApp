from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from apps.profile.models import Profile
from apps.user_settings.models import UserSettings

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home:home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")

        if User.objects.filter(username=username).exists():
            return render(request, "register/register.html", {"error": "Username already exists."})

        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        Profile.objects.create(user=user, full_name=f"{first_name} {last_name}".strip(), bio="Student Document Requester")
        UserSettings.objects.create(user=user)

        return redirect("login:login")
    return render(request, "register/register.html")