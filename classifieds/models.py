import os

from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Ad.Status.PUBLISHED)


class Ad(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PD', 'Published'

    title = models.CharField(max_length=50)
    slug = models.SlugField(db_index=True,
                            blank=True,
                            editable=False)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='ads')
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE,
                                 related_name='ads')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    region = models.ForeignKey('Region',
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='ads')
    city = models.ForeignKey('City',
                             on_delete=models.SET_NULL,
                             null=True,
                             related_name='ads')
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
        constraints = [
            models.UniqueConstraint(fields=['author', 'slug'], name='unique_author_slug')
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to='core/category_icons/')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Subcategory(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE,
                                 related_name='subcategories')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


def ad_images_upload_to(instance, filename):
    """
    Returns the path to save the image:
    ads/images/YYYY/MM/DD/<ad_id/<filename>
    """
    date_path = now().strftime('%Y/%m/%d')
    return os.path.join('ads', 'images', date_path, str(instance.ad.id), filename)


class AdImage(models.Model):
    ad = models.ForeignKey('Ad',
                           on_delete=models.CASCADE,
                           related_name='images'
                           )
    image = models.ImageField(upload_to=ad_images_upload_to)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.ad.title}_{self.pk}'


class Region(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey('Region',
                        on_delete=models.CASCADE,
                        related_name='cities')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
