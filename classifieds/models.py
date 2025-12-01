from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Ad.Status.PUBLISHED)


class Ad(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PD', 'Published'

    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=65,
                            db_index=True,
                            blank=True,
                            editable=False)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='ads')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='ads')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    views_qty = models.IntegerField(default=0, verbose_name='Views quantity')
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    is_promoted = models.BooleanField(default=False)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)
        indexes = [
            models.Index(fields=['-publish'])
        ]
        unique_together = ('author', 'slug')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
