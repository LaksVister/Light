from django.db import models
from threading import Thread
from catalog.management.commands.get_books import run_crawler

# Create your models here.


class Task(models.Model):

    CHOICES = [
        ('run_scraper', 'Run Scraper'),
        ('count_images', 'Show count images')
    ]

    task = models.CharField(max_length=255, choices=CHOICES)
    arg = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.task

    # def save(self, *args, **kwargs):
    #     result = super().save(*args, **kwargs)
    #
    #     if not self.working:
    #         try:
    #             start, end = self.arg.split(',')
    #             start, end = int(start), int(end)
    #         except Exception as e:
    #             print(e, type(e))
    #             start, end = 0, 10
    #
    #     Thread(target=run_crawler, args=(start, end, self)).start()
    #     return result
