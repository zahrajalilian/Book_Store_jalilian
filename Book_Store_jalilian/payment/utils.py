import json
from .models import *
from accounts.models import *
from book.models import *

def cookieCart(request):
    # Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('CART:', cart)

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']

    for i in cart:
        # We use try block to prevent items in cart that may have been removed from causing error
        try:
            if (cart[i]['quantity'] > 0):  # items with negative quantity = lot of freebies
                cartItems += cart[i]['quantity']

                book= Book.objects.get(id=i)
                total = (book.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'id': book.id,
                    'book': {'id': book.id, 'title': book.title, 'price': book.price,
                                'image': book.image}, 'quantity': cart[i]['quantity'],
                                'get_total': total,
                }
                items.append(item)


        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Invoice.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = CustomUser.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Invoice.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        book = Book.objects.get(id=item['id'])
        orderItem = InvoiceLine.objects.create(
            book=book,
            invoice=order,
            quantity=(item['quantity'] if item['quantity'] > 0 else -1 * item['quantity']),
            # negative quantity = freebies
        )
    return customer, order