# Generated by Django 2.2.6 on 2019-10-20 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20191020_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published', models.DateTimeField(auto_created=True)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('comment', models.TextField()),
                ('rating', models.IntegerField()),
                ('moderated', models.BooleanField(default=False)),
            ],
        ),
    ]
