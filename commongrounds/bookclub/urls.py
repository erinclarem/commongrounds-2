from django.urls import path
from .views import BooksListView, BookDetailView, BookCreateView, BookUpdateView

urlpatterns = [
    path('books', BooksListView.as_view(), name="books_list"),
    path('book/<int:pk>', BookDetailView.as_view(), name="book_detail"),
    path('book/add', BookCreateView.as_view(), name="book_create.html"),
    path('book/<int:pk>/edit', BookUpdateView.as_view(), name="book_update.html"),
]

app_name = 'bookclub'
