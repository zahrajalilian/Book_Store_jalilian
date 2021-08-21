from django.urls import path
from .views import *
from accounts.signup import Signup
from accounts.login import logout,Login
from payment.views import Cart, CheckOut,Index,store,OrderView

from middlewares.auth import  auth_middleware



urlpatterns = [
    # pages
    # path('',home, name='home'),
    path('', Index.as_view(), name='homepage'),
    path('store/', store , name='store'),
    path('listall/', BookListView.as_view(), name='listbook'),
    path('books/<slug>', BookSlugDetailView.as_view()),
    path('books/<pk>', BookDetailView.as_view(),name='book_detail'),
    path('booksbytitle/',SearchBookByTitle,name='book_title'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('cart/', auth_middleware(Cart.as_view()), name='cart'),
    path('check-out', CheckOut.as_view(), name='checkout'),
    path('orders/', auth_middleware(OrderView.as_view()), name='orders'),



]








