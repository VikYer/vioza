from django.contrib import admin

from .models import Ad, Category, Subcategory, AdImage, Region, City


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publish', 'is_promoted', 'views_qty',
                    'favorites_ads')
    list_filter = ('category', 'is_promoted', 'status', 'publish',)
    search_fields = ('title', 'description', 'author__username')
    ordering = ('-publish',)
    list_display_links = ('title',)
    readonly_fields = ('views_qty', 'status', 'created', 'publish', 'updated',)
    list_editable = ('is_promoted',)

    def favorites_ads(self, obj):
        return obj.favorites.count()

    favorites_ads.short_description = 'Favorites'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'icon',)
    search_fields = ('title',)
    ordering = ('title',)
    list_display_links = ('title',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug')
    search_fields = ('title',)
    ordering = ('title',)
    list_display_links = ('title',)


@admin.register(AdImage)
class AdImageAdmin(admin.ModelAdmin):
    list_display = ('ad', 'id', 'is_main')
    list_filter = ('ad', 'is_main')
    readonly_fields = ('id',)
    list_display_links = ('ad',)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    list_filter = ('region',)
