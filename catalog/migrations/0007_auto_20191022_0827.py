# Generated by Django 2.2.6 on 2019-10-22 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_reviews_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='published',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
