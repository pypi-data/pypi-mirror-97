import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class EmailOnline(models.Model):
    id = models.UUIDField(primary_key=True, verbose_name=_("Email ID"), default=uuid.uuid4)
    message_subject = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Email subject"))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User"), null=True, blank=True
    )
    content = models.TextField(null=False, verbose_name=_("Email content"))
    message_date = models.DateTimeField(null=False, blank=False, default=timezone.now)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _("Email online")
        verbose_name_plural = _("Emails online")
