from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile

class Command(BaseCommand):
    help = 'Create missing Profile objects for users who do not have one.'

    def handle(self, *args, **kwargs):
        created_count = 0
        for user in User.objects.all():
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} missing profiles.')) 