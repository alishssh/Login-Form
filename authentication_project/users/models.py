from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class RegisteredUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='registered_user')
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Registered on {self.registration_date}"

    class Meta:
        db_table = 'registered_users'
        ordering = ['-registration_date']

class Profile(models.Model):
    PROVINCE_CHOICES = [
        ('bagmati', 'Bagmati'),
        ('lumbini', 'Lumbini'),
        ('koshi', 'Koshi'),
    ]
    
    DISTRICT_CHOICES = [
        ('kathmandu', 'Kathmandu'),
        ('bhaktapur', 'Bhaktapur'),
        ('lalitpur', 'Lalitpur'),
    ]
    
    MUNICIPALITY_CHOICES = [
        ('gokarneshwor', 'Gokarneshwor'),
        ('thimi', 'Thimi'),
        ('thecho', 'Thecho'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    
    # Address Information
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES, null=True, blank=True)
    district = models.CharField(max_length=50, choices=DISTRICT_CHOICES, null=True, blank=True)
    municipality = models.CharField(max_length=50, choices=MUNICIPALITY_CHOICES, null=True, blank=True)
    ward_number = models.IntegerField(null=True, blank=True)
    street_name = models.CharField(max_length=200, null=True, blank=True)
    house_number = models.CharField(max_length=50, null=True, blank=True)
    
    # Additional Information
    grandfather_name = models.CharField(max_length=100, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    citizenship_number = models.CharField(max_length=50, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Add this new model for additional credentials
class AdditionalCredentials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    security_question = models.CharField(max_length=100)
    security_answer = models.CharField(max_length=100)
    secondary_email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    preferred_login_method = models.CharField(
        max_length=20,
        choices=[
            ('email', 'Email'),
            ('phone', 'Phone'),
            ('both', 'Both Email and Phone')
        ],
        default='email'
    )
    
    def __str__(self):
        return f'{self.user.username} Additional Credentials'
