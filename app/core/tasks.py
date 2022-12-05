import datetime

from app import settings
from celery import shared_task
from django.core.mail import send_mail


from django.contrib.auth.models import User
from core.models import Transaction


MESSAGE_TRANSACTION_FORMAT = '-----------------------------\n' \
                             'Organization: {organization}\n' \
                             '{category}\n' \
                             'Amount: {amount}\n' \
                             'Description:\n' \
                             '{description}\n' \
                             '-----------------------------\n'


@shared_task(bind=True)
def send_mail_task(self):
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)

    mail_subject = 'Expense statistic'

    users = User.objects.all()
    
    for user in users:
        to_email = user.email
        if to_email:
            transactions = Transaction.objects.filter(created_at__gte=date_from)
            message = 'Statistic\n'
            for transaction in transactions:
                message += MESSAGE_TRANSACTION_FORMAT.format(
                    organization=transaction.organization,
                    category=transaction.category,
                    amount=transaction.amount,
                    description=transaction.description
                )
            send_mail(
                subject=mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=False
            )
