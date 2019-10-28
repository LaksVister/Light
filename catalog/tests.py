from django.test import TestCase, RequestFactory
from .models import *
from .management.commands.get_books import crawler, urls_generator
from .views import HomeView
from task.models import Task


class BookTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_urls_generator(self):
        task = Task.objects.create(task='asd')
        gen = urls_generator(0, 10, task)
        result = list(gen)
        self.assertEqual(len(result), 10)

    def test_crawler(self):
        count = Book.objects.all().count()
        self.assertEqual(count, 0)
        url = 'https://openlibrary.org/books/OL1M/'
        crawler(url)
        count = Book.objects.all().count()
        self.assertEqual(count, 1)

    def test_book_structure(self):
        name = hasattr(Book, 'name')
        slug = hasattr(Book, 'slug')
        description = hasattr(Book, 'description')
        img = hasattr(Book, 'img')
        language = hasattr(Book, 'language')
        places = hasattr(Book, 'places')
        self.assertTrue(name)
        self.assertTrue(slug)
        self.assertTrue(description)
        self.assertTrue(img)
        self.assertTrue(language)
        self.assertTrue(places)

    def test_home_view(self):
        request = self.factory.get('/')
        home_obj = HomeView()
        home_obj.request = request
        results_context = home_obj.get_context_data()
        self.assertTrue('len_users' in results_context)
