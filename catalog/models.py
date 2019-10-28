from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    img = models.ImageField(upload_to='books_images')
    language = models.CharField(max_length=255)
    places = models.CharField(max_length=255)
    times = models.CharField(max_length=255)
    published = models.CharField(max_length=255, null=True, blank=True)

    pages = models.CharField(max_length=255)

    # ID Numbers
    openlibrary = models.CharField(max_length=255)
    archive = models.CharField(max_length=255)
    isbn10 = models.CharField(max_length=255)
    isbn13 = models.CharField(max_length=255)

    img_source = models.URLField(max_length=255, null=True)
    book_source = models.URLField(max_length=255, null=True, blank=True)

    parsing_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    categs = models.ManyToManyField(Category)
    authors = models.ManyToManyField(Author)
    users = models.ManyToManyField(User)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Reviews(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField()
    comment = models.TextField()
    rating = models.IntegerField()
    published = models.DateTimeField(auto_now_add=True)
    moderated = models.BooleanField(default=False)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.name
