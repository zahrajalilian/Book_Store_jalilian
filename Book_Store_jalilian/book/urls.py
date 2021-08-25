from django.urls import path
from .views import *
urlpatterns = [
    path('', BookListView.as_view(), name='listbook'),
    path('books/<slug>', BookDetailView,name='book_detail'),
    path('booksbytitle/', SearchBookByTitle, name='book_title'),
    ]


