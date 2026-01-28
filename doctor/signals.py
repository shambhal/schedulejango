from django.contrib.auth.models import User
from django.db.models.signals import post_save
from  appoint.utils.dates import Util
from  .models import Notification,Book
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.template.loader import get_template

import logging

logger = logging.getLogger(__name__)
@receiver(post_save, sender=Notification)
def notify_send_mail(sender, instance, created, **kwargs):
    
       context={
      'dated':Util.convertDate(instance.book.dated),
      'slot':Util.to_ampm(instance.book.slot),
      'desc':instance.book.desc,
      "extra_info":instance.book.extra_info,
      'status':instance.book.status,
      'name':instance.book.name
       }
       message = get_template("mail/book_notification.html").render(context)
       print(message)
       logger.log(1,message)
@receiver(post_save, sender=User)
def create_user_password_and_email(sender, instance, created, **kwargs):
    if created:
        # Generate a random password
        password = get_random_string(length=8)  # or any desired length

        # Set the password"
        instance.set_password(password)
        instance.save()

        logger.log(logging.INFO, f"{password} saved as password")
        return

        # Send email to user
        send_mail(
            subject="Your Account Password",
            message=f"Hello {instance.username},\n\nYour password is: {password}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )
