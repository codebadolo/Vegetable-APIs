import random
from django.core.management.base import BaseCommand
from orders.models import Transaction, Order
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create random transactions for orders'

    def handle(self, *args, **kwargs):
        orders = Order.objects.all()

        if not orders.exists():
            self.stdout.write(self.style.ERROR('No orders found.'))
            return

        for order in orders:
            transaction = Transaction.objects.create(
                transaction_id=f'TXN-{random.randint(1000, 9999)}',
                order=order,
                amount=order.total_price,  # Set the transaction amount to the order total
                status=random.choice(['pending', 'completed', 'failed']),
                created_at=timezone.now()
            )
            self.stdout.write(self.style.SUCCESS(f'Created transaction "{transaction.transaction_id}" for order "{order.id}".'))

        self.stdout.write(self.style.SUCCESS('Transactions created successfully.'))
