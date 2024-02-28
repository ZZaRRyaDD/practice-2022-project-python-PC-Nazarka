from django.contrib import admin

from ..models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    """Admin class for Quote model."""

    list_display = (
        'id',
        'text',
        'author',
    )
    list_filter = (
        'text',
        'author',
    )
    search_fields = (
        'text',
        'author',
    )
