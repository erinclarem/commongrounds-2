from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Book, Bookmark, BookReview, Borrow
from accounts.mixins import RoleRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BookForm, BookReviewForm, BookBorrowForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone


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

        context['is_bookmarked'] = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context['is_bookmarked'] = Bookmark.objects.filter(
                profile=profile).filter(book=self.get_object()).exists()

        context['is_contributor'] = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context['is_contributor'] = self.get_object().contributor.filter(
                id=profile.id).exists()

        context['book_reviews'] = BookReview.objects.filter(
            book=self.get_object())

        return context

    def post(self, request, *args, **kwargs):
        if 'submit_bookmark' in request.POST:
            bookmark = Bookmark.objects.filter(
                book=self.get_object(),
                profile=self.request.user.profile
            )

            if bookmark.exists():
                bookmark.delete()
            else:
                Bookmark.objects.create(
                    book=self.get_object(),
                    profile=self.request.user,
                    date_bookmarked=timezone.now()
                )
            return redirect(self.get_success_url())

        elif 'submit_review' in request.POST:
            review_form = BookReviewForm(request.POST, request.FILES)
            if review_form.is_valid():
                if BookReview.objects.filter(reviewer=self.request.user.profile).filter(book=self.get_object()).exists():
                    book_review = BookReview.objects.get(
                        reviewer=self.request.user.profile, book=self.get_object())
                    book_review.delete()
                else:
                    if self.request.user.is_authenticated:
                        review_form.instance.user_reviewer = self.request.user.profile
                    else:
                        review_form.instance.anon_reviewer = 'Anonymous'
                review = review_form.save(commit=False)
                review.reviewer = self.request.user.profile
                review.book = self.get_object()
                review.save()
                return redirect(self.get_success_url())
            else:
                return self.render_to_response(
                    self.get_context_data(review_form=review_form)
                )

        return self.get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('bookclub:book_detail',
                            kwargs={'pk': self.kwargs['pk']})


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
            borrow.date_to_return = borrow.date_borrowed + \
                timezone.timedelta(14)
            borrow.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form)
            )
