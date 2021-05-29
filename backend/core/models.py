from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateField("Дата создания", auto_now_add=True)
    modified = models.DateField("Дата изменения", auto_now=True)

    class Meta:
        abstract = True