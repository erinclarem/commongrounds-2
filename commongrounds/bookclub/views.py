from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Book, Bookmark, BookReview, Borrow
from accounts.mixins import RoleRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BookForm, BookReviewForm, BookBorrowForm
from django.shortcuts import redirect


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


class BookCreateView(RoleRequiredMixin, LoginRequiredMixin, CreateView):
    model = Book
    template_name = "book_create.html"
    form_class = BookForm
    required_role = "Book Contributor"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.get_object().contributor = self.request.user.profile
        return response


class BookUpdateView(RoleRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Book
    template_name = "book_update.html"
    form_class = BookForm
    required_role = "Book Contributor"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.get_object().save()
        return response


class BookBorrowView(DetailView):
    model = Borrow
    template_name = "book_borrow.html"
    form_class = BookBorrowForm

    def post(self, request, *args, **kwargs):
        borrowed_book = self.get_object().book
        form = BookBorrowForm(request.POST)
        borrow = form.save(commit=False)
        if form.is_valid():
            if self.request.user.is_authenticated:
                borrow.borrower = self.request.user.profile
            borrow.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form)
            )
