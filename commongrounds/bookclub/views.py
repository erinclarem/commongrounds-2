from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Book, Bookmark, BookReview
from accounts.mixins import RoleRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BookReviewForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookmarks = 0
        for book in Bookmark.objects.filter(book=self.get_object()):
            bookmarks += 1
        context['bookmarks'] = bookmarks

        context['is_contributor'] = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context['is_contributor'] = self.get_object().contributor.filter(
                id=profile.id).exists()

        context['book_reviews'] = BookReview.objects.filter(
            book=self.get_object())

    form_class = BookReviewForm

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            form.instance.user_reviewer = self.request.user.profile
        else:
            form.instance.anon_reviewer = 'Anonymous'
        return response

    def get_success_url(self):
        return reverse('bookclub:detail', kwargs={'pk': self.object.pk})
