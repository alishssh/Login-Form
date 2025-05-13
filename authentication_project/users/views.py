from users.models import Profile, AdditionalCredentials, RegisteredUser
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm, AdditionalCredentialsForm
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.utils import timezone

@csrf_protect
def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            try:
                # Create the user
                user = user_form.save()
                
                # Create and save the profile
                profile, created = Profile.objects.get_or_create(user=user)
                profile.first_name = profile_form.cleaned_data.get('first_name')
                profile.middle_name = profile_form.cleaned_data.get('middle_name')
                profile.last_name = profile_form.cleaned_data.get('last_name')
                profile.province = profile_form.cleaned_data.get('province')
                profile.district = profile_form.cleaned_data.get('district')
                profile.municipality = profile_form.cleaned_data.get('municipality')
                profile.ward_number = profile_form.cleaned_data.get('ward_number')
                profile.street_name = profile_form.cleaned_data.get('street_name')
                profile.house_number = profile_form.cleaned_data.get('house_number')
                profile.grandfather_name = profile_form.cleaned_data.get('grandfather_name')
                profile.father_name = profile_form.cleaned_data.get('father_name')
                profile.citizenship_number = profile_form.cleaned_data.get('citizenship_number')
                profile.save()

                # Create registered user record
                RegisteredUser.objects.create(
                    user=user,
                    phone=user_form.cleaned_data.get('phone'),
                    email=user_form.cleaned_data.get('email')
                )

                messages.success(request, f'Account created for {user.username}! You can now log in.')
                return redirect('login')
            except Exception as e:
                # If there's an error, delete the user and show error message
                if user:
                    user.delete()
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
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
    redirect_authenticated_user = False
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        # Update last login time in RegisteredUser
        try:
            registered_user = self.request.user.registered_user
            registered_user.last_login = timezone.now()
            registered_user.save()
        except RegisteredUser.DoesNotExist:
            pass
        return reverse_lazy('home')

@login_required
def home_view(request):
    if request.method == 'POST':
        try:
            profile = request.user.profile
            # Update profile fields
            profile.first_name = request.POST.get('first_name')
            profile.middle_name = request.POST.get('middle_name')
            profile.last_name = request.POST.get('last_name')
            profile.province = request.POST.get('province')
            profile.district = request.POST.get('district')
            profile.municipality = request.POST.get('municipality')
            profile.ward_number = request.POST.get('ward_number')
            profile.street_name = request.POST.get('street_name')
            profile.house_number = request.POST.get('house_number')
            profile.grandfather_name = request.POST.get('grandfather_name')
            profile.father_name = request.POST.get('father_name')
            profile.citizenship_number = request.POST.get('citizenship_number')
            
            profile.save()
            messages.success(request, 'Profile updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
    
    return render(request, 'home.html', {
        'profile': request.user.profile
    })


def agreement_view(request):
    return render(request, 'users/agreement.html')


@login_required
def additional_credentials(request):
    # Check if user already has additional credentials
    try:
        credentials = AdditionalCredentials.objects.get(user=request.user)
        # If credentials exist, pre-populate the form
        if request.method == 'POST':
            form = AdditionalCredentialsForm(request.POST, instance=credentials)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your additional credentials have been updated!')
                return redirect('home')
        else:
            form = AdditionalCredentialsForm(instance=credentials)
    except AdditionalCredentials.DoesNotExist:


        # If credentials don't exist, create new ones
        if request.method == 'POST':
            form = AdditionalCredentialsForm(request.POST)
            if form.is_valid():
                credentials = form.save(commit=False)
                credentials.user = request.user
                credentials.save()
                messages.success(request, 'Your additional credentials have been saved!')
                return redirect('home')
        else:
            form = AdditionalCredentialsForm()
    
    return render(request, 'users/additional_credentials.html', {'form': form})
