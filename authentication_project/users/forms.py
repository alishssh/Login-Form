from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, AdditionalCredentials

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # Add tailwind classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            if field_name == 'username':
                field.help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
            elif field_name == 'password1':
                field.help_text = 'Your password must contain at least 8 characters.'
            elif field_name == 'password2':
                field.help_text = 'Enter the same password as before, for verification.'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        # Add tailwind classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        # Add tailwind classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name', 'middle_name', 'last_name',
            'province', 'district', 'municipality',
            'ward_number', 'street_name', 'house_number',
            'grandfather_name', 'father_name', 'citizenship_number'
        ]
        widgets = {
            'province': forms.Select(choices=Profile.PROVINCE_CHOICES),
            'district': forms.Select(choices=Profile.DISTRICT_CHOICES),
            'municipality': forms.Select(choices=Profile.MUNICIPALITY_CHOICES),
            'ward_number': forms.NumberInput(),
            'citizenship_number': forms.NumberInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = (
                'w-full px-3 py-2 border border-gray-300 '
                'rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            )

class AdditionalCredentialsForm(forms.ModelForm):
    class Meta:
        model = AdditionalCredentials
        fields = ['security_question', 'security_answer', 'secondary_email', 
                  'phone_number', 'preferred_login_method']
        widgets = {
            'security_answer': forms.PasswordInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(AdditionalCredentialsForm, self).__init__(*args, **kwargs)
        # Add tailwind classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
