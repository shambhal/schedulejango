from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from orders.models import Order

class Command(BaseCommand):
    help = "Expire orders older than 7 days"

    def handle(self, *args, **kwargs):
        threshold = timezone.now() - timedelta(days=7)

        qs = Order.objects.filter(
            updated_at__lt=threshold
        ).exclude(status='EXPIRED')

        count = qs.update(status='EXPIRED')

        self.stdout.write(self.style.SUCCESS(
            f"{count} orders expired"
        ))
