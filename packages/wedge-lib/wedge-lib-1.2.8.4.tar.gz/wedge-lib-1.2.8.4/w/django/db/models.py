from django.db import models


class AbstractCreatedUpdatedModel(models.Model):
    modified = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
