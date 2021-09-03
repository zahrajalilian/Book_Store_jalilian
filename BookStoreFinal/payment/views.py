from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .models import *
from .forms import OrderForm,CouponForm
from cart.models import Cart
from discount.models import BasketDiscount
# Create your views here.
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from suds import Client


@login_required(login_url='login')
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    forms = CouponForm()
    return render(request, 'order.html', {'order': order, 'forms': forms})


"""
create 
cart == prod in cart get
delete when form checked
"""

# /////////////////////////////////

def order_create(request):
    """
    rder create
    :param request:
    :return:
    """
    try:
        customer = request.user
    except:
        device = request.COOKIES['device']
        customer, created = CustomUser.objects.get_or_create(device=device)

    if request.method == 'POST':
        froms = OrderForm(request.POST)

        if froms.is_valid():
            data = froms.cleaned_data

            order = Order.objects.create(customer=customer, email=data['email'],
                                        f_name=data['f_name'], l_name=data['l_name'], address=data['address'])

            cart = Cart.objects.filter(customer=customer)
            for c in cart:
                ItemOrder.objects.create(order_id=order.id, customer_id=customer.id,
                                         product_id=c.product_id, quantity=c.quantity
                                         )
            Cart.objects.filter(customer_id=customer.id).delete()
            return redirect('order_detail', order.id)


"""
require_POST == if req is post
use when just post
check coupon
"""


@require_POST
def coupon_order(request,order_id):
    """
    adding coupon to our total price
    :param request:
    :param order_id:
    :return:
    """
    form = CouponForm(request.POST)
    time = timezone.now()
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = BasketDiscount.objects.get(code_discount__iexact=code,
                                                validate_date__lte=time, expire_date__gte=time, active=True)
        except BasketDiscount.DoesNotExist:
            messages.error(request, 'this code is not valid', 'danger')
            return redirect('order_detail', order_id)
        order = Order.objects.get(id=order_id)
        order.discount_code = coupon.percent_discount
        order.save()
    return redirect('order_detail', order_id)

# ///////////////////////////////////////////

def order_history(request):
    """
    order history
    :param request:
    :return:
    """
    try:
        customer = request.user
    except:
        device = request.COOKIES['device']
        customer, created = CustomUser.objects.get_or_create(device=device)
    orders = Order.objects.filter(customer=customer)
    return render(request, 'history.html', {'orders':orders})

# ///////////////////////////////

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'jalilian.zahra97@gmail.com'  # Optional
mobile = '09199574362'  # Optional
CallbackURL = 'http://localhost:8000/verify/' # Important: need to edit for realy server.


def send_request(request,price,order_id):
    """
    send request
    :param request:
    :param price:
    :param order_id:
    :return:
    """
    global amount
    amount = price
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        order = Order.objects.get(id=order_id)
        order.paid = True
        order.save()
        cart=ItemOrder.objects.filter(order_id=order_id)
        for c in cart:
            product = Book.objects.get(id=c.product_id)
            product.inventory -= c.quantity
            product.save()
        # return HttpResponse('Error code: ' + str(result.Status))
        messages.success(request, 'پرداخت با موفقیت انجام شد')
        return HttpResponse('پرداخت با موفقیت انجام شد')


"""
verify our account
"""
def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            return HttpResponse('Transaction success.')
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')