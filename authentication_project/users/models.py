from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# Signal to create or update the profile when the user is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # If the user is being created, create a profile for them
    if created:
        Profile.objects.create(user=instance)
    else:
        # If the profile already exists, update it
        instance.profile.save()
