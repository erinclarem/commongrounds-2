from django.db import models
from django.urls import reverse
from accounts.models import Profile


class Genre (models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'
        ordering = ['name']


class Book (models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='books'
    )
    contributor = models.ForeignKey(
        Profile,
        null=True,
        related_name='books'
    )
    author = models.CharField(max_length=100)
    synopsis = models.TextField()
    publication_year = models.IntegerField()
    available_to_borrow = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('bookclub:book_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'
        ordering = ['-publication_year']


class BookReview (models.Model):
    user_reviewer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        related_name='book reviews'
    )
    anon_reviewer = models.TextField()
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        null=True,
        related_name='book reviews'
    )
    title = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return f"{self.title}"


class Bookmark (models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        related_name='bookmarks'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        null=True,
        related_name='bookmarks'
    )
    date_bookmarked = models.DateField()


class Borrow (models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        null=True,
        related_name='borrows'
    )
    borrower = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        related_name='borrows'
    )
    name = models.CharField(max_length=100)
    date_borrowed = models.DateField()
    date_to_return = models.DateField()
