import sys
from datetime import datetime
from slugify import slugify
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

from requests_html import HTMLSession
from django.core.management.base import BaseCommand

from catalog.models import *

locker = Lock()


def crawler(url):
    with HTMLSession() as session:
        response = session.get(url)

    def checker(xpath: str):
        try:
            return response.html.xpath(xpath)[0].text
        except Exception as e:
            print(e, type(e), sys.exc_info()[-1].tb_lineno)
            return '-'

    isbn10 = '-'
    isbn13 = '-'
    openlibrary = '-'
    archive = '-'

    name = checker('//h1[@itemprop="name"]')

    slug = slugify(name)

    description = checker('//div[@class="editionAbout"]//p[1]').strip()

    description = ''.join([f'<p>{p}<p>' for p in description.split('\n') if p])

    img_source = response.html.xpath('//img[@itemprop="image"]/@src')[0]
    print('link image:', img_source)
    if img_source:
        if img_source[:2] == '//':
            img_source = img_source.replace('//', 'http://')

    try:

        with HTMLSession() as session2:
            img_resp = session2.get(img_source)

        image_name = 'books_images/' + slug + img_source[-4:]

        with open(f'media/{image_name}', 'wb') as imgf:
            imgf.write(img_resp.content)

        del img_resp

    except Exception as e:
        print(e, type(e), sys.exc_info()[-1].tb_lineno)
        image_name = 'books_images/book-404.png'

    language = checker('//a[@href="/languages/eng"]')
    places = checker('(//div[@class="section link-box"]//span)[3]')
    times = checker('(//div[@class="section link-box"]//span)[4]')

    pages = checker('//dd[@itemprop="numberOfPages"]')

    # ID Numbers
    try:

        if response.html.xpath('//dt[text()="Open Library"]'):
            openlibrary = checker('//h3[text()="ID Numbers"]/following-sibling::dd[1]')

        if response.html.xpath('//dt[text()="Internet Archive"]'):
            archive = checker('(//dd[@class="object"]//a)[1]')

        # For situation 1:
        # ISBN 10
        # ISBN 13
        if response.html.xpath('//dt[text()="ISBN 10"]'):
            isbn10 = checker('(//dd[@itemprop="isbn"])[1]')
        elif response.html.xpath('//dt[text()="ISBN 13"]'):
            isbn13 = checker('(//dd[@itemprop="isbn"])[2]')

        # For situation 2:
        # ISBN 13
        # ISBN 10
        if response.html.xpath('//dt[text()="ISBN 13"]'):
            isbn13 = checker('(//dd[@itemprop="isbn"])[2]')
        elif response.html.xpath('//dt[text()="ISBN 10"]'):
            isbn10 = checker('(//dd[@itemprop="isbn"])[1]')

        categs = response.html.xpath('(//div[@class="section link-box"]//span)[1]')[0].text.strip().split(',')
        authors = response.html.xpath('//a[@itemprop="author"]')[0].text.strip().split(',')
        users = response.html.xpath('//a[@itemprop="publisher"]')[0].text.strip().split(',')

    except Exception as e:
        print(e, type(e), sys.exc_info()[-1].tb_lineno)

    published = checker("//strong[@itemprop='datePublished']")

    book = {
        'name': name,
        'slug': slug,
        'description': description,
        'img_source': img_source,
        'book_source': url,
        'language': language,
        'places': places,
        'times': times,

        'pages': pages,

        'openlibrary': openlibrary,
        'archive': archive,
        'isbn10': isbn10,
        'isbn13': isbn13,

        'img': image_name,
        'published': published
    }

    try:

        with locker:
            book = Book.objects.create(**book)

        for cate in categs:
            cate = {'name': cate, 'slug': slugify(cate), 'description': ''}
            with locker:
                cate, created = Category.objects.get_or_create(**cate)
            book.categs.add(cate)

        for author in authors:
            author = {'name': author, 'slug': slugify(author)}
            with locker:
                author, created = Author.objects.get_or_create(**author)
            book.authors.add(author)

        for user in users:
            user = {'name': user, 'slug': slugify(user)}
            with locker:
                user, created = User.objects.get_or_create(**user)
            book.users.add(user)

    except Exception as e:
        print(e, type(e))
        return

    print('Success:', url)


def urls_generator(start, end, task):
    for i in range(start, end):
        url = f'https://openlibrary.org/books/OL{i}M/'
        with locker:
            task.status = f'scrape id: {i}'
            task.save()
        yield url


def run_crawler(start, end, task):
    task.status = 'start parsing'
    task.save()
    url_gen = urls_generator(start, end, task)
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(crawler, url_gen)
    task.status = 'finished'
    task.end_time = datetime.now()
    task.save()


class Command(BaseCommand):
    help = 'Running books scraper'

    def handle(self, *args, **options):
        from task.models import Task

        task = Task.objects.create(name='run_scraper')
        run_crawler(0, 100000, task)


