from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
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
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    
    # Address Information
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES)
    district = models.CharField(max_length=50, choices=DISTRICT_CHOICES)
    municipality = models.CharField(max_length=50, choices=MUNICIPALITY_CHOICES)
    ward_number = models.IntegerField()
    street_name = models.CharField(max_length=200)
    house_number = models.CharField(max_length=50)
    
    # Additional Information
    grandfather_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    citizenship_number = models.CharField(max_length=50)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save() 