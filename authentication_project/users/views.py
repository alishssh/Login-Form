from users.models import Profile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm 

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()  # Save the user
            
            # Prevent creating a profile if one already exists
            profile, created = Profile.objects.get_or_create(user=user)
            
            # Update profile if needed
            if not created:
                profile_form.instance = profile
                profile_form.save()  # Save the profile

            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileUpdateForm()

    return render(request, 'users/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

def home_view(request):
    return render(request, 'home.html')