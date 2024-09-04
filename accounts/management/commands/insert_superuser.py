from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = "inserting superuser"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        User.objects.create_superuser(
            phone_number="09351234567", password="1234"
        )
