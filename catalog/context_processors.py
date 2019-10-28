from django.db.models import Count
from .models import Category
from cache_memoize import cache_memoize


@cache_memoize(60*60)
def menu(request):
    categories = Category.objects.annotate(
        books_count=Count('book')).order_by('-books_count')[:5]
    return {
        'categories': categories,
    }
