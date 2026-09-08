from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def home_view(request):
    return render(request, 'accounts/home.html')