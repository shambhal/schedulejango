from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order, OrderItems, OrderHistory, OS_CHOICES
from doctor.models import Book
from cart.models import Cart as AppCart
from django.conf import settings
from datetime import date
import logging
#from config import EMAIL_ADMIN
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def order_updated(sender, instance, created, **kwargs):
    # print("signal processed")
    # print(created)
    logger.warning(instance.status)
    logger.warning(kwargs)
    order_id = instance.id
    order = Order.objects.get(pk=order_id)
    if order:
        items = OrderItems.objects.filter(order_id=order)
        # bh=BookHistory.objects.all.filter(order_id=order_id,status=instance.status).get()
        for item in items:
            """""" """adding booking"""
            bo = Book.objects.all().filter(order_item_id=item.id)
            if not bo.exists() :
                bo2 = Book(slot=item.slot, dated=item.dated, doctor_id=item.doctor_id)
                bo2.order_item_id = item.id
                bo2.desc = item.doctor+' - '+item.category
                bo2.order_id = order.id
                bo2.name = order.name
                bo2.phone = order.phone
                bo2.email = order.email
                bo2.doctor_id=item.doctor_id
                bo2.device_id = order.device_id
                bo2.status = instance.status
                bo2.save()
    oh = OrderHistory.objects.filter(order=order).last()
    if oh is None:
        oh = OrderHistory(order=order, status=instance.status)
        oh.save()
    else:
        if oh.status != instance.status:
            oh = OrderHistory(order=order, status=instance.status)
            oh.save()

'''
@receiver(post_save, sender=Book)
def sendmail(sender, instance, created, **kwargs):
    book_id = instance.id
    binfo = Book.objects.get(pk=book_id)
    # if not binfo.ex
    #   return
    if binfo:
        message = get_template("mail/book.html").render(Context({"order": binfo}))
        mail = EmailMessage(
            subject="Appointment confirmation",
            body=message,
            from_email=settings.EMAIL_ADMIN,
            to=[binfo.email],
            reply_to=[settings.EMAIL_ADMIN],
        )
        mail.content_subtype = "html"
        return mail.send()
'''

@receiver(post_save, sender=Book)
def clear_cart(sender, instance, created, **kwargs):
    book_id = instance.id
    binfo = instance
    # if not binfo.ex
    #   return
    if binfo:
        ap = AppCart.objects.filter(
            user_id=binfo.user_id,
            dated=binfo.dated,
            slot=binfo.slot,
            device_id=binfo.device_id
        ).delete()


@receiver(post_save, sender=Order)
def order_success(sender, instance, created, **kwargs):
    if instance.status != "COMPLETED":
        return

    flag = True
    
    for oitem in OrderItems.objects.filter(order_id=instance.id):
     try:
        bo = Book.objects.filter(order_item_id=oitem.id).first()
        if not bo:
            already_booked = Book.objects.filter(
                dated=oitem.dated,
                slot=oitem.slot,
                doctor_id=oitem.doctor_id,
                status="BOOKED"
            ).exists()

            bo = Book(
                dated=oitem.dated,
                slot=oitem.slot,
                status="DECLINED" if already_booked else "BOOKED",
                user_id=instance.user_id,
                order_item_id=oitem.id,
                order_id=instance.id,
                doctor_id=oitem.doctor_id,
                device_id=instance.device_id,
                email=instance.email,
                desc=f"{oitem.doctor} - {oitem.category}",
                name=instance.name,
                phone=instance.phone,
            )
        else:
            # If already exists, just reconfirm status
            already_booked = Book.objects.filter(
                dated=oitem.dated,
                slot=oitem.slot,
                doctor_id=oitem.doctor_id,
                status="BOOKED"
            ).exclude(id=bo.id).exists()

            bo.status = "DECLINED" if already_booked else "BOOKED"

        bo.save()

           
           

     except Exception as e:
            logging.error(f"Booking failed for order_item {oitem.id}: {e}")
            flag = False

    OrderHistory.objects.create(
        dated=date.today(),
        order_id=instance.id,
        status="COMPLETED" if flag else "PARTIALLY_COMPLETED",
    )
