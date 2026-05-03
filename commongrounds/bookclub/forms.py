from django import forms
from .models import Book, Bookmark, BookReview


class BookForm(forms.ModelForm):
    class Meta:
        fields = ['title', 'genre', 'author', 'synopsis',
                  'publication_year', 'available_to_borrow']


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['title', 'comment']
