# Generated by Django 2.2.6 on 2019-10-20 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20191020_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
