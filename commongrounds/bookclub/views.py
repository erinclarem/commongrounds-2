from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Book, Bookmark, BookReview


class BooksListView(ListView):
    model = Book
    template_name = "books_list.html"

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_books'] = Book.objects.all()
        if self.request.user.is_authenticated:
            context['contributed_books'] = Book.objects.filter(
                contributor=self.request.user.profile
            )
            context['bookmarked_books'] = Book.objects.filter(
                bookmarks__profile=self.request.user.profile
            )
            context['reviewed_books'] = Book.objects.filter(
                book_reviews__user_reviewer=self.request.user.profile
            )
            context['all_books'] = Book.objects.exclude(
                contributor=self.request.user.profile
            ).exclude(
                bookmarks__profile=self.request.user.profile
            ).exclude(
                book_reviews__user_reviewer=self.request.user.profile
            )
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"
