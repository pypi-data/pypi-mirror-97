from django.db import models


class TextChoices(models.TextChoices):
    @classmethod
    def list_codes(cls):
        return [code for code, label in cls.choices]


class AbstractCreatedUpdatedModel(models.Model):
    created_at = models.DateTimeField("crée le", auto_now_add=True)
    updated_at = models.DateTimeField("maj le", auto_now=True)

    class Meta:
        abstract = True


class Reference(AbstractCreatedUpdatedModel):
    code = models.CharField(max_length=20, primary_key=True)
    label = models.CharField(max_length=100)

    class Meta:
        abstract = True
        ordering = ["label"]

    def __str__(self):
        return self.label
