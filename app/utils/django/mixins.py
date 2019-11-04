from django.conf import settings
from django.db import models
from django.utils import timezone

__all__ = (
    'DeletedFlagManager',
    'DeletedFlagMixin',
    'DeletedUserRequiredException',
)


class DeletedFlagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class DeletedUserRequiredException(Exception):
    pass


class DeletedFlagMixin(models.Model):
    """
    삭제시 DB에서 실제로 삭제되는 것이 아니라 is_deleted및 deleted_on필드를 값을 기록하도록 하는 Mixin
    """
    DELETED_USER_REQUIRED = False

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='삭제한 사용자', on_delete=models.SET_NULL,
                                   null=True)

    class Meta:
        abstract = True

    def perform_delete(self):
        pass

    def delete(self, deleted_user=None, *args, **kwargs):
        if self.DELETED_USER_REQUIRED and not deleted_user:
            raise DeletedUserRequiredException()
        if deleted_user:
            self.deleted_by = deleted_user
        self.is_deleted = True
        self.perform_delete()
        self.deleted_on = timezone.now()
        self.save()
