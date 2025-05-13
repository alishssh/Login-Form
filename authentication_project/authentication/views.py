from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

@login_required
def home(request):
    if request.method == 'POST':
        try:
            profile = request.user.profile
            
            # Update personal information
            profile.first_name = request.POST.get('first_name')
            profile.middle_name = request.POST.get('middle_name')
            profile.last_name = request.POST.get('last_name')
            
            # Update address information
            profile.province = request.POST.get('province')
            profile.district = request.POST.get('district')
            profile.municipality = request.POST.get('municipality')
            profile.ward_number = request.POST.get('ward_number')
            profile.street_name = request.POST.get('street_name')
            profile.house_number = request.POST.get('house_number')
            
            # Update additional information
            profile.grandfather_name = request.POST.get('grandfather_name')
            profile.father_name = request.POST.get('father_name')
            profile.citizenship_number = request.POST.get('citizenship_number')
            
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
    
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('login') 