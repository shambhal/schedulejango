from django.test import TestCase
from .models import Book,Notification
from django.template.loader import get_template

import logging

logger = logging.getLogger(__name__)

# Create your tests here.
class NotificationModelTest(TestCase):
    def test_notification_creation():
        bk=Book.objects.create(
            dated="2026-01-16",
            desc="Appointment with Dcotor Malti Shamrma",
                               name="Siddharth Singh Chauhan",
                               extra_info="Really works",
                               email="shambhalnetworks@gmail.com",
                               phone="9786783838",
                               status='BOOKED',
                               doctor_id=8,
                               order_item_id=8,

                               
                               slot="11:00-12:00")
        notif=Notification.objects.create(book=bk,type="mail")
        context={
      'dated':notif.book.dated,
      'slot':notif.book.slot,
      'desc':notif.book.desc,
      "extra_info":notif.book.extra_info,
      'status':notif.book.status
       }
        message = get_template("mail/book.html").render(context)
        logger.info(message)
        print(message)
        #self.assertTrurue)