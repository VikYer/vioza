from django.contrib import admin

from .models import Ad, Category, Subcategory


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publish', 'is_promoted', 'views_qty',)
    list_filter = ('category', 'is_promoted', 'status', 'publish',)
    search_fields = ('title', 'description', 'author__username')
    ordering = ('-publish',)
    list_display_links = ('title',)
    readonly_fields = ('views_qty', 'status', 'created', 'publish', 'updated',)
    list_editable = ('is_promoted',)


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
