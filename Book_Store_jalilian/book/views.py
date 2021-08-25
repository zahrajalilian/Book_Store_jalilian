from django.shortcuts import render
from django.shortcuts import get_object_or_404
# Create your views here.
# from django.template.context_processors import request
from django.views.generic import ListView, DetailView
from .models import Book
from cart.models import *


class BookListView(ListView):
    # paginate_by = 2
    model = Book
    template_name = 'home.html'
    queryset = Book.objects.order_by('-created_at')
    context_object_name = 'products'


#


def BookDetailView(request, slug):
    product = get_object_or_404(Book,slug=slug)
    cart_form = CartForm
    return render(request,'book_detail.html',{'product':product,
                                              'cart_form':cart_form})


"""
search data by title,author
"""
from django.db.models import Q


def SearchBookByTitle(request):
    q = request.GET['query']

    products=Book.objects.filter(Q(title__icontains=q) | Q(author__full_name__icontains=q))

    mydictionary = {

        "products" :products,
    }
    return render(request,'home.html',context=mydictionary)


