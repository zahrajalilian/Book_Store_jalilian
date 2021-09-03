
from django.shortcuts import render, redirect
from book.models import Book
from accounts.models import CustomUser, Address
from .models import Cart, CartForm
from django.contrib.auth.decorators import login_required
from payment.forms import OrderForm


@login_required(login_url='login')
def cart_detail(request):
    """
    cart detail
    :param request:
    :return:
    """
    try:
        customer = request.user


    except:
        device = request.COOKIES['device']
        customer, created = CustomUser.objects.get_or_create(device=device)

    cart = Cart.objects.filter(customer=customer)
    address = Address.objects.filter(user_id=request.user.id)
    form = OrderForm()
    total = 0
    for pro in cart:
        total += pro.product.total_price * pro.quantity
    context = {
        'cart': cart, 'total': total, 'form': form,
        'addresses':address
    }
    return render(request, 'cart.html', context)


"""
add to the cart
1-we must now which product to add to the cart == by get and id =get(id=id)
2- check if product is already in cart to add to or not == filter 
3- check the users ==>customer_id ==> request.id
- check = 1 == yes exist already
- check = 0 == NO ==> create
4- customer chosed == 
valid form
to redirect

"""


@login_required(login_url='login')
def add_cart(request, id):
    """
    a func for adding to cart
    :param request:
    :param id:
    :return:
    """
    url = request.META.get('HTTP_REFERER')
    product = Book.objects.get(id=id)

    try:
        customer = request.user
    except:
        device = request.COOKIES['device']
        customer, created = CustomUser.objects.get_or_create(device=device)

    data = Cart.objects.filter(customer=customer, product_id=product.id)
    if data:
        check = 1
    else:
        check = 0

    if request.method == 'POST':

        froms = CartForm(request.POST)
        if froms.is_valid():
            quan = froms.cleaned_data['quantity']
            if check == 1:
                shop = Cart.objects.get(customer=customer, product_id=id)
                shop.quantity += quan
            else:
                Cart.objects.create(customer=customer, product_id=id, quantity=quan)

        return redirect(url)


@login_required(login_url='login')
def remove_cart(request, id):
    """
    remove from cart
    """

    url = request.META.get('HTTP_REFERER')
    Cart.objects.filter(id=id).delete()
    return redirect(url)



@login_required(login_url='login')
def add_single(request, id):
    """
     add  single
    """
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id=id)
    product = Book.objects.get(id=cart.product.id)
    if product.inventory > cart.quantity:
        cart.quantity += 1
    cart.save()
    return redirect(url)


def remove_single(request,id):
    """
    remove   single
    """
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id=id)
    if cart.quantity <2:
        cart.delete()
    else:
        cart.quantity -= 1
        cart.save()
    return redirect(url)



