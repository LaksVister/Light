from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from catalog.models import *


class BookAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_filter = ['language']
    list_display = ['name', 'slug', 'img_source', 'parsing_date', 'language']
    list_editable = ['slug', 'img_source']
    search_fields = ['description']


class ReviewAdmin(SummernoteModelAdmin):
    summernote_fields = ('comment',)
    list_filter = ['moderated']
    list_display = ['name', 'email', 'moderated']
    search_fields = ['name', 'description']


class CategoriesAdmin(SummernoteModelAdmin):
    search_fields = ['name']


admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoriesAdmin)
admin.site.register(Author)
admin.site.register(User)
admin.site.register(Reviews, ReviewAdmin)
