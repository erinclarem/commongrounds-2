from django import forms
from .models import Book, BookReview, Borrow


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'synopsis',
                  'publication_year', 'available_to_borrow']


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['title', 'comment']


class BookBorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['name', 'date_borrowed']
