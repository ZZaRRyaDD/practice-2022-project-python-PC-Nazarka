from django.db.models import Manager

from ..querysets import TargetQuerySet


class TargetManager(Manager):
    """Class for custom manager of `Target` model."""

    def get_queryset(self, **kwargs):
        return TargetQuerySet(
            self.model,
            using=self._db,
        )
