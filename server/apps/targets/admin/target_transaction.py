from django.contrib import admin

from ..models import TargetTransaction


@admin.register(TargetTransaction)
class TargetTransactionAdmin(admin.ModelAdmin):
    """Admin class for TargetTransaction model."""

    list_display = ('target', 'amount', 'created_at')
    list_filter = ('target', 'amount', 'created_at')
    search_fields = ('target', 'amount', 'created_at')
