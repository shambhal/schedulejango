from django.shortcuts import render
from doctor.models import Book
from orders.models import Order,OrderHistory,OrderItems
# Create your views here.
from django.http import HttpResponse

def test(request):
    order_id=request.GET.get('order_id',0)
    order = Order.objects.get(pk=order_id)
    if order:
        items = OrderItems.objects.filter(order_id=order)
        # bh=BookHistory.objects.all.filter(order_id=order_id,status=instance.status).get()
        for item in items:
            """""" """adding booking"""
            bo = Book.objects.all().filter(order_item_id=item.id)
            if not bo.exists() and (order.status == "PROCESSING"):
                bo2 = Book(slot=item.slot, dated=item.dated, doctor_id=item.doctor_id)
                bo2.order_item_id = item.id
                bo2.desc = item.doctor+' - '+item.category
                bo2.order_id = order.id
                bo2.name = order.name
                bo2.phone = order.phone
                bo2.email = order.email
                bo2.doctor_id=item.doctor_id
                bo2.device_id = order.device_id
                bo2.status = order.status
                bo2.save()
    oh = OrderHistory.objects.filter(order=order).last()
    if oh is None:
        oh = OrderHistory(order=order, status=order.status)
        oh.save()
    else:
        if oh.status != order.status:
            oh = OrderHistory(order=order, status=order.status)
            oh.save()
    return HttpResponse("hat")