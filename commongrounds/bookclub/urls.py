from django.urls import path
from .views import BooksListView, BookDetailView, BookCreateView, BookUpdateView, BookBorrowView

urlpatterns = [
    path('books', BooksListView.as_view(), name="books_list"),
    path('book/<int:pk>', BookDetailView.as_view(), name="book_detail"),
    path('book/add', BookCreateView.as_view(), name="book_create"),
    path('book/<int:pk>/edit', BookUpdateView.as_view(), name="book_update"),
    path('book/<int:pk>/borrow', BookBorrowView.as_view(), name="book_borrow"),
]

app_name = 'bookclub'
