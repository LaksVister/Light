# Generated by Django 2.2.6 on 2019-10-18 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parsing_date', models.DateTimeField(auto_created=True, blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('img', models.ImageField(upload_to='books_images')),
                ('language', models.CharField(max_length=255)),
                ('places', models.CharField(max_length=255)),
                ('times', models.CharField(max_length=255)),
                ('pages', models.CharField(max_length=255)),
                ('openlibrary', models.CharField(max_length=255)),
                ('archive', models.CharField(max_length=255)),
                ('isbn10', models.CharField(max_length=255)),
                ('isbn13', models.CharField(max_length=255)),
                ('img_source', models.URLField(default='https://lh5.googleusercontent.com/aQq5deLpM3CfdPe3T-5W9AlSPmNWVVBD1zMhssgx6F-9k1UPJ5_gDUEeTJg_lvyPS3zYWKbTUtJ_NY4mW-_f=w1920-h950', max_length=255)),
                ('book_source', models.URLField(blank=True, max_length=255, null=True)),
                ('authors', models.ManyToManyField(to='catalog.Author')),
                ('categs', models.ManyToManyField(to='catalog.Category')),
                ('users', models.ManyToManyField(to='catalog.User')),
            ],
        ),
    ]