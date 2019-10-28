# Generated by Django 2.2.6 on 2019-10-22 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20191022_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='img_source',
            field=models.URLField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='parsing_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
