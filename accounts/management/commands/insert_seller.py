from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = "inserting seller"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        numbers = ['09121234567', '09121234598', '09121634598']
        for number in numbers:
            if not User.objects.filter(phone_number=number).exists():
                User.objects.create_seller(
                    phone_number=number, password="1234"
                )
