from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
# Create your views here.
# from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Book, Author, Category
from cart.models import *


from django.contrib.auth.mixins import PermissionRequiredMixin


class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):

        if (not self.request.user.is_authenticated):
            return redirect_to_login(self.request.get_full_path(),self.get_login_url(),
                                     self.get_redirect_field_name())
        if not self.has_permission():

            return redirect('home')
        return super(UserAccessMixin, self).dispatch(request,*args,**kwargs)


# /////////////////////////////////////////////////////////////////


class BookListView(ListView):
    # paginate_by = 2
    model = Book
    template_name = 'home.html'
    queryset = Book.objects.order_by('-created_at')
    context_object_name = 'products'


def BookDetailView(request, slug):
    product = get_object_or_404(Book,slug=slug)
    cart_form = CartForm
    return render(request, 'book_detail.html', {'product': product,
                                              'cart_form': cart_form})


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


# ///////////////////////////////////////////////////////
# add /delete/change/view
class BookCreateView(UserAccessMixin, CreateView):
    permission_required = 'book.add_Book'
    permission_denied_message = ' sorry cant access to this page'
    model = Book
    template_name = 'book_new.html'
    fields = ['title', 'description', 'author', 'inventory', 'category','unit_price','discount','image','document_addr']


class BookUpdateView(UserAccessMixin, UpdateView):
    permission_required = 'book.change_Book'
    permission_denied_message = ' sorry cant access to this page'
    model = Book
    template_name = 'book_edit.html'
    fields = ['title', 'description', 'inventory', 'unit_price', 'category', 'discount', 'author']


class BookDeleteView(UserAccessMixin, DeleteView):
    permission_required = 'book.delete_Book'
    permission_denied_message = ' sorry cant access to this page'
    model = Book
    template_name = 'book_delete.html'
    success_url = reverse_lazy('home')
# /////////////////////////////////////////////////////


class AuthorListViewAdmin(UserAccessMixin,ListView):
    permission_required = ('book.delete_Author','book.view_Author')
    permission_denied_message = ' sorry cant access to this page'
    model = Author
    template_name = 'all_author_admin.html'
    context_object_name = 'authors'


class AuthorCreateView( CreateView):
    model = Author
    fields = ['full_name']
    template_name = 'author_new.html'
    success_url = reverse_lazy('home')

class AuthorDeleteView(UserAccessMixin, DeleteView):
    permission_required = 'book.delete_Author'
    permission_denied_message = ' sorry cant access to this page'
    model = Author
    template_name = 'author_delete.html'
    success_url = reverse_lazy('home')
#     /////////////////////////////////////////


# class CategoryCreateView(UserAccessMixin, CreateView):
class CategoryCreateView( CreateView):
    # permission_required = 'book.add_Category'
    # permission_denied_message = ' sorry cant access to this page'
    model = Category
    fields = ['name']
    template_name = 'category_new.html'


class CategoryDeleteView(UserAccessMixin, DeleteView):
    permission_required = 'book.delete_Category'
    permission_denied_message = ' sorry cant access to this page'
    model = Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('home')

# /////////////////////////////////////////////////////////////


class BookListViewAdmin(UserAccessMixin,ListView):
    permission_required = ('book.delete_Book','book.change_Book','book.view_Book')
    permission_denied_message = ' sorry cant access to this page'
    model = Book
    template_name = 'all_book_admin.html'
    queryset = Book.objects.order_by('-created_at')
    context_object_name = 'products'


class CategoryListViewAdmin(ListView):

    model = Category
    template_name = 'all_category.html'
    context_object_name = 'category'
