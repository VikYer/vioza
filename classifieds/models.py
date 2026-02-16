import os
from io import BytesIO
from unicodedata import category

from django.core.cache import cache
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now
from django.urls import reverse

from PIL import Image, ImageOps
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Ad.Status.PUBLISHED)


class Ad(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PD', 'Published'
        ARCHIVED = 'AR', 'Archived'
        EXPIRED = 'EX', 'Expired'

    title = models.CharField(max_length=50)
    slug = models.SlugField(db_index=True,
                            blank=True,
                            editable=False)
    main_page = models.ForeignKey(
        'AdImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='ads')
    show_phone = models.BooleanField(default=False)
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE,
                                 related_name='ads')
    subcategory = models.ForeignKey('Subcategory',
                                    on_delete=models.SET_NULL,
                                    blank=True,
                                    null=True,
                                    related_name='ads')
    price = models.DecimalField(max_digits=10,
                                validators=[MinValueValidator(0)],
                                decimal_places=2)
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       blank=True,
                                       related_name='favorite_ads')
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
    tags = TaggableManager(blank=True)

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

    def get_absolute_url(self):
        return reverse(
            'ads:ad_detail',
            args=[
                self.slug,
                self.pk
            ]
        )


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to='core/category_icons/')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        result = super().save(*args, **kwargs)
        cache.delete('categories_with_subcategories')
        return result

    def delete(self, *args, **kwargs):
        result = super().delete(*args, **kwargs)
        cache.delete('categories_with_subcategories')
        return result

    def get_absolute_url(self):
        return reverse(
            'ads:ads_by_category',
            args=[self.slug]
        )


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
        result = super().save(*args, **kwargs)
        cache.delete('categories_with_subcategories')

        return result

    def delete(self, *args, **kwargs):
        result = super().delete(*args, **kwargs)
        cache.delete('categories_with_subcategories')
        return result

    def get_absolute_url(self):
        return reverse(
            'ads:ads_by_subcategory',
            args=[
                self, category.slug,
                self.slug
            ]
        )


def ad_images_upload_to(instance, filename) -> str:
    """
    Returns the path to save the image:
    ads/images/YYYY/MM/DD/<ad_id/<filename>
    """
    date_path = now().strftime('%Y/%m/%d')
    return os.path.join('ads', 'images', date_path, str(instance.ad.id), filename)


def ad_webp_images_upload_to(instance, filename) -> str:
    """
    Returns the path to save the webp image:
    ads/images/YYYY/MM/DD/<ad_id/webp/<filename>
    """
    date_path = now().strftime('%Y/%m/%d')
    return os.path.join('ads', 'images', date_path, str(instance.ad.id), 'webp', filename)


def ad_thumbnail_upload_to(instance, filename) -> str:
    """
    Returns the path to save the thumbnail:
    ads/images/YYYY/MM/DD/<ad_id/thumbs/<filename>
    """
    date_path = now().strftime('%Y/%m/%d')
    return os.path.join('ads', 'images', date_path, str(instance.ad.id), 'thumbs', filename)


class AdImage(models.Model):
    ad = models.ForeignKey('Ad',
                           on_delete=models.CASCADE,
                           related_name='images')
    image = models.ImageField(upload_to=ad_images_upload_to)
    image_webp = models.ImageField(upload_to=ad_webp_images_upload_to,
                                   editable=False,
                                   null=True,
                                   blank=True)
    thumbnail = models.ImageField(upload_to=ad_thumbnail_upload_to,
                                  editable=False,
                                  null=True,
                                  blank=True)

    def __str__(self):
        return f'{self.ad.title}_{self.pk}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_image = None
        if not is_new:
            try:
                old_image = AdImage.objects.get(pk=self.pk).image
            except AdImage.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        if is_new or (old_image and old_image.name != self.image.name):
            self._generate_webp_and_thumbnail()
            super().save(update_fields=['image_webp', 'thumbnail'])

    def _generate_webp_and_thumbnail(self) -> None:
        """Convert image in webp extension and generate 300x300 thumbnail"""
        img = Image.open(self.image.path).convert('RGB')

        # WEBP
        buffer_webp = BytesIO()
        img.save(buffer_webp, format='WEBP', quality=85)
        webp_name = self.image.name.rsplit('.', 1)[0] + f'_{self.pk}.webp'
        self.image_webp.save(webp_name, ContentFile(buffer_webp.getvalue()), save=False)

        # THUMBNAIL 300x300
        thumbnail_img = ImageOps.fit(img, (300, 300), Image.LANCZOS)
        buffer_thumb = BytesIO()
        thumbnail_img.save(buffer_thumb, format='WEBP', quality=85)
        thumb_name = self.image.name.rsplit('.', 1)[0] + f'_{self.pk}_thumb.webp'
        self.thumbnail.save(thumb_name, ContentFile(buffer_thumb.getvalue()), save=False)


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
