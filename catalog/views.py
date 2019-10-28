import logging
from django.shortcuts import render
from django.http import Http404
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from django.contrib import messages

from .models import *


logger = logging.getLogger('django')


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        len_books = Book.objects.all()
        len_authors = Author.objects.all()
        len_users = User.objects.all()
        romance_books = Book.objects.all()[142:150]  # .filter(name__contains = 'romance'  [in stock 3 books])
        fantasy_books = Book.objects.all()[240:248]
        history_books = Book.objects.all()[32:40]
        biographies_books = Book.objects.all()[332:340]
        context.update({
            'len_books': len_books,
            'len_authors': len_authors,
            'len_users': len_users,
            'romance_books': romance_books,
            'fantasy_books': fantasy_books,
            'history_books': history_books,
            'biographies_books': biographies_books,
        })

        logger.debug(context)

        return context


class CatalogView(ListView, SingleObjectMixin):
    template_name = 'catalog.html'
    model = Book
    paginate_by = 9

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            queryset=Category.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        author = self.request.GET.get('author')
        if author:
            return Book.objects.filter(authors__slug=author)
        return Book.objects.filter(categs=self.object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_authors'] = Author.objects.annotate(books_count=Count('book')).order_by('-books_count')[:22]
        return context


@method_decorator(csrf_protect, name='dispatch')
class BookView(DetailView):
    template_name = 'book.html'
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_books'] = Book.objects.all()[:4]
        context['reviews'] = Reviews.objects.filter(
            book=self.object, moderated=True).order_by('-published')[:10]
        return context

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        data = self.request.POST
        review = {
            'name': data['name'],
            'email': data['email'],
            'comment': data['comment'],
            'rating': data['rating'],
            'book': self.object
        }
        Reviews.objects.create(**review)
        messages.add_message(
            self.request, messages.INFO,
            'Thanks! Your review is on moderation.'
        )

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class SearchView(ListView):
    template_name = 'catalog.html'
    model = Book
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query.isdigit():
            return Book.objects.filter(published__contains=query)
        elif query:
            return Book.objects.filter(name__contains=query)
        else:
            return Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_authors'] = Author.objects.annotate(books_count=Count('book')).order_by('-books_count')[:22]
        return context


class SearchDataView(ListView):
    template_name = 'catalog.html'
    model = Book
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Book.objects.filter(published__contains=query)
        else:
            return Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_authors'] = Author.objects.annotate(books_count=Count('book')).order_by('-books_count')[:22]
        return context



def robots_view(request):
    return render(request, 'robots.txt', {}, content_type="text/plain")
