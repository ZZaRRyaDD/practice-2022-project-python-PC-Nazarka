from django.contrib import admin

from ..models import Target


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    """Admin class for Target model."""

    list_display = (
        'name',
        'amount',
        'initial_deposit',
        'deposit_term',
        'percent',
        'user',
    )
    list_filter = (
        'name',
        'amount',
        'initial_deposit',
        'created_at',
    )
    search_fields = (
        'name',
        'amount',
        'initial_deposit',
        'deposit_term',
        'percent',
        'user',
    )
