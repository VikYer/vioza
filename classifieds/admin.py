from django.contrib import admin

from .models import Ad

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publish', 'is_promoted', 'views_qty',)
    list_filter = ('category', 'is_promoted', 'status', 'publish',)
    search_fields = ('title', 'description', 'author__username')
    ordering = ('-publish',)
    list_display_links = ('title',)
    readonly_fields = ('views_qty', 'status', 'created', 'publish', 'updated', )
    list_editable = ('is_promoted',)