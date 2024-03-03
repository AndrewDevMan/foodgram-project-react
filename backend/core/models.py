from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BaseMetaModel(models.Model):
    """Абстрактная базовая модель"""

    class Meta:
        abstract = True
        ordering = ["-id"]
        default_related_name = "%(class)ss"
