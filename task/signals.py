import os
from threading import Thread
from django.db.models.signals import post_save
from .models import Task
from django.conf import settings

from catalog.management.commands.get_books import run_crawler


def handler_tasks(sender, instance, **kwargs):
    if kwargs.get('created'):
        if instance.task == 'run_scraper':
            try:
                start, end = instance.arg.split(',')
                start, end = int(start), int(end)
            except Exception as e:
                print(e, type(e))
                start, end = 0, 100
            Thread(target=run_crawler, args=(start, end, instance)).start()
        elif instance.task == 'count_images':
            count_images = os.listdir(
                os.path.join(settings.BASE_DIR, 'media/books_images'))
            instance.status = f'images: {len(count_images)}'
            instance.save()


post_save.connect(handler_tasks, sender=Task)
