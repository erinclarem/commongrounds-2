from django.contrib import admin
from .models import Book, Genre

class BookInline(admin.TabularInline):
    model = Book

class BookAdmin(admin.ModelAdmin):
    model = Book
    search_fields = ('title', 'genre', 'created_on', 'updated_on')

class GenreAdmin(admin.ModelAdmin):
    model = Genre
    inlines = [BookInline,]

admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)