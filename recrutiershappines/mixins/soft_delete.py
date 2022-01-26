from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.with_deleted = kwargs.pop('deleted', False)
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def _base_queryset(self):
        return super().get_queryset().filter()

    def get_queryset(self):
        qs = self._base_queryset()
        if self.with_deleted:
            return qs
        return qs.filter(deleted_at=None)


class DeletableMixin(models.Model):
    class Meta:
        abstract = True
    objects = SoftDeleteManager()
    objects_with_deleted = SoftDeleteManager(deleted=True)
    deleted_at = models.DateTimeField(null=True, default=None)


    def delete(self, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()
