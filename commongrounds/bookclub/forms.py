from django import forms
from .models import Book, Bookmark, BookReview


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['title', 'comment']
